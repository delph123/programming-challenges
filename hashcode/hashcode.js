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
	
	find() {
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
					picked: false,
					dirty: false,
					reord: false,
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
				this.best.push(record);
			}
		}
		
		this.cache = [];
		for (let i = 0; i < this.config.cache.nb; i++) {
			this.cache[i] = {
				size: 0,
				vid: new Set()
			}
		}
		
		console.log("First sort...");
		this.sort();
		
		this.oldBest = [];
		let r = undefined; var t = 0;		
		while (r = this.pickFirstBoth()) {
			t++;
			console.log("> Solution " + t + " picked. Remaining " + (this.best.length-this.first+this.oldBest.length) + " solutions.")
			r.picked = true;
			this.cache[r.cId].vid.add(r.vId);
			this.cache[r.cId].size += this.config.vid.size[r.vId];
			for (let i = 0; i < this.config.ep.nb; i++) {
				if (this.config.cache.pool[r.cId].ep[i]) {
					this.config.vid.latency[i][r.vId] = this.config.cache.pool[r.cId].ep[i];
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
		
		return this.cache.map((rec) => (rec.vid));
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
		let iTo = mAction.until.split("|").reduce((idx, sep) => {
			let idx2 = this.buffer.indexOf(sep, iFrom);
			if (idx2 < idx && idx2 >= 0) {
				return idx2;
			} else {
				return idx;
			}
		}, this.buffer.length);
		iTo = iTo < 0 ? this.buffer.length : iTo;
		this.cursor = iTo + 1;
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
	
	static read(sInputFilePath) {
		var sBuf = Parser.readInput("./" + sInputFilePath);
		var aRules = Parser.readRules("./rules.json");
		var oParser = new Parser(sBuf, aRules);
		console.log("File " + sInputFilePath + " parsed successfully.");
		var oScorer = new Scorer(oParser.result);
		var oStrategy = new Strategy(oParser.result);
		var aCachingStrategy = oStrategy.find();
		//var aCachingStrategy = oScorer.randCachingStrategy()
		return {
			scorer: oScorer,
			strategy: oStrategy,
			cachingStrategy: aCachingStrategy,
			score: oScorer.score(aCachingStrategy),
			scoreKittens: [0,370175],
			scoreWorth: [603624, 3105],
			scoreTrending: [499801, 47554],
			scoreZoo: [504106, 161465]
		};
	}
	
}

module.exports = {
	Parser : Parser,
	Scorer : Scorer,
	Strategy : Strategy
}
