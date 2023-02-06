const fs = require('fs')

class Strategy {
	
	constructor(mConfig) {
		this.config = mConfig;
		this.first = 0;
	}
	
	score(record) {
		let savings = 0;
		for (let i of record.req) {
			let req = this.config.req.pool[i];
			savings += req.nb * Math.max(this.config.vid.latency[req.epId][record.vId]
											- this.config.cache.pool[record.cId].ep[req.epId], 0);
		}
		record.savings = savings;
		record.score = savings / this.config.vid.size[record.vId];
	}
	
	sort() {
		this.best.sort((a,b) => (b.score - a.score));
		while (this.best.length > 0 && this.best[this.best.length-1].score < 0.001) {
			this.best.pop();
		}
	}
	
	reorderOld(aNew) {
		let aOld = this.oldBest;
		aNew.sort((a,b) => (b.score - a.score));
		this.oldBest = [];
		let a = 0, b = 0;
		while (a < aNew.length && b < aOld.length) {
			if (aOld[b].dirty) {
				b++;
			} else {
				if (aNew[a].score > aOld[b].score) {
					this.oldBest.push(aNew[a]);
					a++;
				} else {
					this.oldBest.push(aOld[b]);
					b++;
				}
			}
		}
		while (a < aNew.length) {
			this.oldBest.push(aNew[a]);
			a++;
		}
		while (b < aOld.length) {
			if (aOld[b].dirty) {
				b++;
			} else {
				this.oldBest.push(aOld[b]);
				b++;
			}
		}
		while (this.oldBest.length > 0 && this.oldBest[this.oldBest.length-1].score < 0.001) {
			this.oldBest.pop();
		}
		aNew.forEach((e) => { e.dirty = false; });
	}
	
	reorder(aNew) {
		let aOld = this.best;
		aNew.sort((a,b) => (b.score - a.score));
		this.best = [];
		let a = 0, b = 0;
		while (a < aNew.length && b < aOld.length) {
			if (aOld[b].dirty) {
				aOld[b].dirty = false;
				b++;
			} else {
				if (aNew[a].score > aOld[b].score) {
					this.best.push(aNew[a]);
					a++;
				} else {
					this.best.push(aOld[b]);
					b++;
				}
			}
		}
		while (a < aNew.length) {
			this.best.push(aNew[a]);
			a++;
		}
		while (b < aOld.length) {
			if (aOld[b].dirty) {
				aOld[b].dirty = false;
				b++;
			} else {
				this.best.push(aOld[b]);
				b++;
			}
		}
		while (this.best.length > 0 && this.best[this.best.length-1].score < 0.001) {
			this.best.pop();
		}
		
	}
	
	pickFirstBoth() {
		while (this.first < this.best.length
				&& ( !this.fitCache(this.best[this.first]) || this.best[this.first].reord || this.best[this.first].picked )) {
			this.first++;
		}
		
		while (this.oldBest.length > 0
				&& ( !this.fitCache(this.oldBest[0]) || this.oldBest[0].picked )) {
			this.oldBest.shift();
		}
		
		if (this.first < this.best.length && this.oldBest.length === 0) {
			this.first++;
			return this.best[this.first-1];
		} else if (this.first < this.best.length && this.oldBest.length > 0) {
			if (this.best[this.first].score >= this.oldBest[0].score) {
				this.first++;
				return this.best[this.first-1];				
			} else {
				return this.oldBest.shift();
			}
		} else if (this.first >= this.best.length && this.oldBest.length > 0) {
			return this.oldBest.shift();
		}
	}
	
	pickFirst() {
		while (this.best.length > 0 && !this.fitCache(this.best[0])) {
			this.best.shift();
		}
		
		if (this.best.length > 0) {
			return this.best.shift();
		}
	}
	
	fitCache(record) {
		return (this.cache[record.cId].size + this.config.vid.size[record.vId]) <= this.config.cache.size;
	}
	
	find(prop = 2, max = 2**30) {
		console.log("Finding solution...");
		this.config.cache.pool = [];
		var pool = this.config.cache.pool;
		console.log("Preparing cache...");
		for (let i = 0; i < this.config.cache.nb; i++) {
			pool[i] = { ep: [], vid: [] };
			for (let j = 0; j < this.config.vid.nb; j++) {
				pool[i].vid[j] = {
					cId: i,
					vId: j,
					req: []
				}
			}
		}
		console.log("Preparing cache end points...");
		for (let i = 0; i < this.config.ep.nb; i++) {
			for (let cache of this.config.ep.pool[i].caches) {
				pool[cache.id].ep[i] = cache.latency;
			}
		}
		console.log("Preparing cache videos...");
		for (let i = 0; i < this.config.req.nb; i++) {
			if (i%1000 === 0) console.log(">", i);
			let req = this.config.req.pool[i];
			let ep = this.config.ep.pool[req.epId];
			for (let cache of ep.caches) {
				pool[cache.id].vid[req.vidId].req.push(i);
			}
		}
		console.log("Preparing latencies...");
		this.config.vid.latency = [];
		for (let i = 0; i < this.config.ep.nb; i++) {
			this.config.vid.latency[i] = [];
			for (let j = 0; j < this.config.vid.nb; j++) {
				this.config.vid.latency[i][j] = this.config.ep.pool[i].latency;
			}
		}
		
		console.log("Preparing best strategy...");
		this.best = [];
		for (let i = 0; i < this.config.cache.nb; i++) {
			for (let j = 0; j < this.config.vid.nb; j++) {
				let record = this.config.cache.pool[i].vid[j];
				this.score(record);
				if (record.score > 0) {
					this.best.push(record);
				}				
			}
		}
		
		this.cache = [];
		for (let i = 0; i < this.config.cache.nb; i++) {
			this.cache[i] = {
				size: 0,
				vid: new Set()
			}
		}
		
		switch (prop) {
			case 1:
				console.log("First sort...");
				this.sort();
				this.findFirst(max);
				break;
			case 2:
				this.findNext(max);
				break;
		}
				
		return this.cache.map((rec) => (rec.vid));
	}
	
	findFirst(max = 2**30) {
		
		this.oldBest = [];
		let r = undefined;
		var t = 0;
		
		while ((t++ < max) && (r = this.pickFirstBoth())) {
			console.log("> Solution " + t + " (" + r.cId + "," + r.vId + "). Remaining " + (this.best.length-this.first+this.oldBest.length) + " solutions.")
			r.picked = true;
			this.cache[r.cId].vid.add(r.vId);
			this.cache[r.cId].size += this.config.vid.size[r.vId];
			for (let i = 0; i < this.config.ep.nb; i++) {
				if (this.config.cache.pool[r.cId].ep[i]) {
					if (this.config.cache.pool[r.cId].ep[i] < this.config.vid.latency[i][r.vId]) {
						this.config.vid.latency[i][r.vId] = this.config.cache.pool[r.cId].ep[i];
					}
				}
			}
			let aChangedElems = [];
			for (let i = 0; i < this.config.cache.nb; i++) {
				if (!this.config.cache.pool[i].vid[r.vId].picked) {
					this.score(this.config.cache.pool[i].vid[r.vId]);
					this.config.cache.pool[i].vid[r.vId].dirty = true;
					this.config.cache.pool[i].vid[r.vId].reord = true;
					aChangedElems.push(this.config.cache.pool[i].vid[r.vId]);
				}
			}
			//this.sort();
			this.reorderOld(aChangedElems);
			//if (t === 3) break;
		}
		
	}
	
	findNext(max = 2**30) {
		
		let r = undefined;
		let t = 0;
		
		console.log("Building heap...")
		let h = new Heap(this, this.best);
		this.best.forEach((e,i) => { e.idx = i; });
		
		while ((t++ < max) && (r = h.pickFirst())) {
			console.log("> Solution " + t + " (" + r.cId + "," + r.vId + "). Remaining " + h.last + " solutions.");
			this.cache[r.cId].vid.add(r.vId);
			this.cache[r.cId].size += this.config.vid.size[r.vId];
			for (let i = 0; i < this.config.ep.nb; i++) {
				if (this.config.cache.pool[r.cId].ep[i]) {
					if (this.config.cache.pool[r.cId].ep[i] < this.config.vid.latency[i][r.vId]) {
						this.config.vid.latency[i][r.vId] = this.config.cache.pool[r.cId].ep[i];
					}
				}
			}
			for (let i = 0; i < this.config.cache.nb; i++) {
				if (this.config.cache.pool[i].vid[r.vId].score > 0) {
					this.score(this.config.cache.pool[i].vid[r.vId]);
					//this.config.cache.pool[i].vid[r.vId].score = 0;
					h.reorder(this.config.cache.pool[i].vid[r.vId])
				}
			}
		}
		
	}
	
}

class Heap {
		
	constructor(oStrategy, aTable) {
		this.strategy = oStrategy;
		this.table = aTable;
		this.last = aTable.length;
		this.build();
	}
		
	pickFirst() {
		while (this.last > 0 && !this.strategy.fitCache(this.table[0])) {
			this.remove(0);
		}
		
		if (this.last > 0) {
			return this.remove(0);
		}
	}
	
	reorder(record) {
		if (record.score < 0.01) {
			this.remove(record.idx);
		} else {
			this.down(record.idx);
		}
	}
	
	remove(index) {
		if (index > 0) {
			this.table[index].score = this.table[0].score + 1;
			this.up(index);
		}
		
		this.last--;
		this.table[0].score = -1;
		this.swap(0, this.last);
		
		this.down(0);
		return this.table[this.last];
	}
		
	build() {
		let n = 2 ** Math.trunc(Math.log2(this.last)) - 2;
		for (let i = n; i >= 0; i--) {
			this.down(i);
		}
	}
	
	up(index) {
		let i = index;
		let j = Math.trunc((i-1)/2);
		while (i > 0 && this.table[j].score < this.table[i].score) {
			this.swap(i, j);
			i = j;
			j = Math.trunc((i-1)/2);
		}
	}
	
	down(index) {
		let i = index;
		let j = 2 * i + 1;
		if (j+1 < this.last && this.table[j].score < this.table[j+1].score) {
			j++;
		}
		while (j < this.last && this.table[i].score < this.table[j].score) {
			this.swap(i, j);
			i = j;
			j = 2 * i + 1;
			if (j+1 < this.last && this.table[j].score < this.table[j+1].score) {
				j++;
			}
		}
	}
	
	swap(i, j) {
		if (i !== j) {
			let t = this.table[i];
			this.table[i] = this.table[j];
			this.table[i].idx = i;
			this.table[j] = t;
			this.table[j].idx = j;
		}
	}
	
	check() {
		for (let i = 1; i < this.last; i++) {
			let j = Math.trunc((i-1)/2);
			if (this.table[i].score > this.table[j].score) {
				console.log("> Big problem :", i, j);
			}
		}
	}
	
	toString() {
		return '[' + this.table.map(e => e.score).join(' ') + '] (0..' + this.last + ')';
	}
	
}

class Scorer {
	
	constructor(mConfig) {
		this.config = mConfig;
	}
	
	score(aCachingStrategy) {
		var savings = 0;
		var sumReq = 0
		for (let req of this.config.req.pool) {
			sumReq += req.nb;
			let ep = this.config.ep.pool[req.epId];
			let latSaved = 0;
			for (let cache of ep.caches) {
				if (aCachingStrategy[cache.id].has(req.vidId)) {
					let newLat = ep.latency - cache.latency;
					if (newLat > latSaved) {
						latSaved = newLat;
					}
				}
			}
			savings += req.nb * latSaved;
		}
		return Math.trunc((1000 * savings) / sumReq);
	}
	
	totalSize(aVids) {
		var sum = 0;
		for (let vId of aVids.values()) {
			sum += this.config.vid.size[vId]
		}
		return sum;
	}
	
	randCachingStrategy() {
		var aCaching = [];
		for (let i = 0; i < this.config.cache.nb; i++) {
			aCaching[i] = new Set();
			for (let n = 0; n < 10; n++) {
				let c = Math.trunc( Math.random() * this.config.vid.nb )
				if (aCaching[i].has(c))
					continue;
				if ( this.totalSize(aCaching[i]) + this.config.vid.size[c]
						<= this.config.cache.size ) {
					aCaching[i].add(c);
				}
			}
		}
		return aCaching;
	}
	
}

class Parser {
	
	constructor(sBuf, aRules) {
		this.buffer = sBuf;
		this.rules = aRules;
		this.cursor = 0;
		this.currentPath = [];
		this.result = {};
		this.parse(this.rules);
	}
	
	parse(aRules) {
		for (let mAction of aRules) {
			let oldPath = this.currentPath;
			this.currentPath = this.computePath(this.currentPath, mAction.target);
			this[mAction.action].call(this, mAction);
			this.currentPath = oldPath;
		}
	}
	
	computePath(aRoot, sRelativePath) {
		var aNewPath = Array.from(aRoot);
		var aRelativePath = sRelativePath.split('/');
		for (let attr of aRelativePath) {
			if (attr === "..") {
				aNewPath.pop();
			} else if (attr !== ".") {
				aNewPath.push(attr);
			}
		}
		return aNewPath;
	}
	
	read(mAction) {
		let iFrom = this.cursor;
		let iTo = iFrom;
		if (mAction.length) {
			iTo = iFrom + mAction.length;
			this.cursor = iTo;
		} else {
			iTo = mAction.until.split("|").reduce((idx, sep) => {
				let idx2 = this.buffer.indexOf(sep, iFrom);
				if (idx2 < idx && idx2 >= 0) {
					return idx2;
				} else {
					return idx;
				}
			}, this.buffer.length);
			iTo = iTo < 0 ? this.buffer.length : iTo;
			this.cursor = iTo + 1;
		}
		let sBuf = this.buffer.substring(iFrom, iTo);
		let _value = undefined;
		if (typeof mAction.parse === "string") {
			_value = this[mAction.parse].call(this, undefined, sBuf)
		} else {
			if (mAction.parse.replace) {
				sBuf = this.parseReplace(mAction.parse.replace, sBuf);
			}
			_value = this[mAction.parse.action].call(this, mAction.parse, sBuf);
		}
		this.set(".", _value);
	}
	
	repeat(mAction) {
		this.set(".", []);
		let times = mAction.times;
		if (typeof mAction.times === "string") {
			times = this.get(mAction.times);
		}
		console.log("In", this.currentPath.join('/'), "looping", times, "times");
		for (let i = 0; i < times; i++) {
			if (i > 0 && i % 1000 === 0) {
				console.log("> loop", i);
			}
			this.currentPath = this.computePath(this.currentPath, "" + i);
			this.parse(mAction.do);
			this.currentPath = this.computePath(this.currentPath, "..");
		}
	}
	
	parseReplace(mParams, sBuf) {
		let aSubst = [];
		if (Array.isArray(mParams)) {
			aSubst = mParams;
		} else {
			aSubst.push(mParams);
		}
		
		return aSubst.reduce((sBuf, {from, to}) => sBuf.replace(new RegExp(from, 'g'), to), sBuf);
	}
	
	parseInt(mParams, sInteger) {
		return parseInt(sInteger);
	}
	
	parseFloat(mParams, sFloat) {
		return parseFloat(sFloat);
	}
	
	parseString(mParams, sString) {
		return sString;
	}
	
	parseBoolean(mParams, sBoolean) {
		return Boolean(sBoolean);
	}
	
	get(sPath) {
		let oCurrent = this.result;
		let aPath = this.computePath(this.currentPath, sPath);
		console.log("Reading", aPath.join('/'));
		for (let attr of aPath) {
			try {
				oCurrent = oCurrent[attr];
			} catch (e) {
				return undefined;
			}
		}
		return oCurrent;
	}
	
	set(sPath, _value) {
		let oCurrent = this.result;
		let aPath = this.computePath(this.currentPath, sPath);
		let sFinalAttr = aPath[aPath.length - 1];
		for (let i = 0; i < aPath.length - 1; i++) {
			let attr = aPath[i];
			// Create necessary object along the requested path.
			if (oCurrent[attr] === undefined || oCurrent[attr] === null) {
				if (aPath[i+1].search(/^(0|([1-9][0-9]*))$/) >= 0) {
					// Next attribute in the path is an integer,
					// create a table instead of an object.
					oCurrent[attr] = [];
				} else {
					oCurrent[attr] = {};
				}
			}
			// Navigate the path.
			if (typeof oCurrent[attr] === "object") {
				oCurrent = oCurrent[attr];
			} else {
				throw "wrong path"
			}
		}
		// Finally, set requested value.
		oCurrent[sFinalAttr] = _value;
	}
	
	static readInput(sPath) {
		return fs.readFileSync(sPath, 'utf-8');
	}
	
	static readRules(sPath) {
		return JSON.parse(fs.readFileSync(sPath, 'utf-8'));
	}
	
	static read(sInputFilePath, prop = 2, max = 2**30) {
		var sBuf = Parser.readInput("./" + sInputFilePath);
		var aRules = Parser.readRules("./rules.json");
		var oParser = new Parser(sBuf, aRules);
		console.log("File " + sInputFilePath + " parsed successfully.");
		var oScorer = new Scorer(oParser.result);
		var oStrategy = new Strategy(oParser.result);
		var aCachingStrategy = oStrategy.find(prop, max);
		var u = oStrategy.cache.map(e => e.size).reduce((a,b) => a+b);
		var t = oStrategy.config.cache.nb * oStrategy.config.cache.size;
		var s = oScorer.score(aCachingStrategy);
		//var aCachingStrategy = oScorer.randCachingStrategy()
		return {
			scorer: () => oScorer,
			strategy: () => oStrategy,
			cachingStrategy: () => aCachingStrategy,
			usage: u,
			total: t,
			not_used: t - u,
			ratio: 100 * u / t,
			score: s,
			score_ratio: s / u,
			max_score: (s/u)*t,
			scoreKittens: [1021680, 370175, 1021811],
			scoreWorth: [608310, 3105, 608522],
			scoreTrending: [499906, 47554, 501140],
			scoreZoo: [507906, 161465, 542634],
			scoreTotal: [2637802, 582299, 2674107]
		};
	}
	
	static playAll(prop = 2, max = 2**30) {
		var aFiles = ["me_at_the_zoo", "videos_worth_spreading", "trending_today", "kittens"];
		var mScores = { total: 0 };
		var aRules = Parser.readRules("./rules.json");
		
		for (let f of aFiles) {
			let sBuf = Parser.readInput("./" + f + ".in");
			let oParser = new Parser(sBuf, aRules);
			console.log("File " + f + " parsed successfully.");
			let oScorer = new Scorer(oParser.result);
			let oStrategy = new Strategy(oParser.result);
			let aCachingStrategy = oStrategy.find(prop, max);
			let s = oScorer.score(aCachingStrategy);
			mScores[f] = s;
			mScores.total += s;
		}
		
		return mScores;
	}
	
}

console.log("node --max_old_space_size=6000 hashcode.js");

console.log(Parser.playAll());
/*
module.exports = {
	Heap: Heap,
	Parser : Parser,
	Scorer : Scorer,
	Strategy : Strategy
}
*/
