//PhantomJs evaluate 获取源代码
var page = require('webpage').create();
var url = "http://www.baidu.com";
page.open(url, function(status) {
	if (status === "success") {
		title = page.evaluate(function() {
			return document.title;
		})
		console.log('Page title is ' + title);
	}
	phantom.exit();
});
