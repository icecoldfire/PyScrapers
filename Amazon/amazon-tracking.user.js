// ==UserScript==
// @name        Amazon Tracking
// @namespace   https://stijngoethals.tk/
// @description Add links to package trackers
// @include     https://www.amazon.*/gp/your-account/ship-track/*
// @version     1.0.2
// @grant       none
// @downloadURL https://raw.githubusercontent.com/icecoldfire/WebsiteScripts/master/Amazon/amazon-tracking.user.js
// ==/UserScript==
(function () {
	'use strict';
	var countryCode = "BE"
	var postalCode = "2180"
	var bPostPatt = new RegExp(/\d{24}/);
	var postnlPatt = new RegExp(/[A-Z0-9]{15}/)
	var element = window.document.getElementsByClassName('a-row a-spacing-top-mini a-size-small a-color-tertiary ship-track-grid-subtext') [0];
	var text = element.innerText;
	var patt;
	var URL;
	var shippingCode;
	if (bPostPatt.test(text)) {
		patt = bPostPatt;
		shippingCode = text.match(patt) [0];
		URL = 'http://track.bpost.be/btr/web/#/search?itemCode=' + shippingCode + '&lang=nl';
	}else if(postnlPatt.test(text)){
		patt = postnlPatt;
		shippingCode = text.match(patt) [0];
		URL = 'https://www.internationalparceltracking.com/Main.aspx#/track/' + shippingCode + '/' + countryCode + '/' + postalCode;
	}else{
		return;
	}
	var a = '<a href="' + URL + '">' + shippingCode + '</a>';
	element.innerHTML = element.innerHTML.replace(patt, a);
}());
