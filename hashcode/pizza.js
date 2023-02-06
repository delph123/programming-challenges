const fs = require('fs')

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
		//console.log(mAction);
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
		//console.log(iFrom,iTo,sBuf);
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
		var aRules = Parser.readRules("./rules2.json");
		var oParser = new Parser(sBuf, aRules);
		console.log("File " + sInputFilePath + " parsed successfully.");
		return oParser.result;
	}
	
}

console.log(Parser.read("example.in"));

/*
module.exports = {
	Heap: Heap,
	Parser : Parser,
	Scorer : Scorer,
	Strategy : Strategy
}
*/
