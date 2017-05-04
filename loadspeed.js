var page = require('webpage').create(),
	system = require('system'),
	t,
	address;

if (system.args.length === 1) {
	//判断参数的多少，命令行传参的知识点。phantomjs loadspeed.js[this is arg 0] http://xxx.com[this is arg 1]
	console.log('Usage: loadspeed.js <some URL>');
	phantom.exit();
}

t = Date.now();
address = system.args[1];
page.open(address, function(status) {
	if (status != 'success') {
		console.log('load failed');
	} else {
		t = Date.now() - t;
		console.log('Loading ' + system.args[1]);
		console.log('cost time ' + t)
	}
	phantom.exit();
});