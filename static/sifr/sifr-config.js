/*****************************************************************************
It is adviced to place the sIFR JavaScript calls in this file, keeping it
separate from the `sifr.js` file. That way, you can easily swap the `sifr.js`
file for a new version, while keeping the configuration.

You must load this file *after* loading `sifr.js`.

That said, you're of course free to merge the JavaScript files. Just make sure
the copyright statement in `sifr.js` is kept intact.
*****************************************************************************/

var gotham08 = {
  src: '/static/sifr/gotham08.swf'
};

var gotham10 = {
  src: '/static/sifr/gotham10.swf'
};

var gotham11 = {
  src: '/static/sifr/gotham11.swf'
};

var gotham02 = {
  src: '/static/sifr/gotham02.swf'
};

var gotham03 = {
  src: '/static/sifr/gotham03.swf'
};

var gotham04 = {
  src: '/static/sifr/gotham04.swf'
};

// You probably want to switch this on, but read <http://wiki.novemberborn.net/sifr3/DetectingCSSLoad> first.
sIFR.useStyleCheck = true;
sIFR.activate(gotham08);
sIFR.activate(gotham10);
sIFR.activate(gotham11);
sIFR.activate(gotham02);
sIFR.activate(gotham03);
sIFR.activate(gotham04);

sIFR.replace(gotham08, {
  selector: 'h1',
  wmode: 'transparent',
  css: {
	'.sIFR-root': { 'opacity': '.8', 'color': '#64802b', 'text-transform': 'uppercase' }
  },
filters: {
	DropShadow: {
	   distance: 1
	  ,color: '#000'
	  ,strength: 1
	  ,alpha: .0
	  ,angle: 30
	  ,knockout: false
	} 

  }
});

sIFR.replace(gotham11, {
  selector: '.step h3',
  wmode: 'transparent',
  css: {
	'.sIFR-root': { 'opacity': '.8', 'color': '#a3a488' }
  }
});

sIFR.replace(gotham11, {
  selector: '.step h2',
  wmode: 'transparent',
  css: {
	'.sIFR-root': { 'opacity': '.4', 'color': '#000000' }
  }
});

sIFR.replace(gotham08, {
  selector: '.certificate h2',
  wmode: 'transparent',
  css: {
	'.sIFR-root': { 'opacity': '.9', 'color': '#cecfaa', 'text-align': 'center' }
  },
  filters: {
	DropShadow: {
	   distance: 1
	  ,color: '#000'
	  ,strength: 1
	  ,alpha: .5
	  ,angle: 30
	  ,knockout: false
	}
  }
});

sIFR.replace(gotham02, {
  selector: 'h2.really',
  wmode: 'transparent',
  css: {
	'.sIFR-root': { 'color': '#ffffff' }
  },
  filters: {
	DropShadow: {
	   distance: 1
	  ,color: '#000000'
	  ,strength: 1
	  ,alpha: 0.5
	  ,angle: 30
	  ,knockout: false
	}
  }
});

sIFR.replace(gotham08, {
  selector: 'h2.neutral',
  wmode: 'transparent',
  css: {
	'.sIFR-root': { 'color': '#ffffff' }
  },
  filters: {
	DropShadow: {
	   distance: 1
	  ,color: '#000000'
	  ,strength: 1
	  ,alpha: 0.5
	  ,angle: 30
	  ,knockout: false
	}
  }
});

sIFR.replace(gotham08, {
  selector: 'h2.congrats',
  wmode: 'transparent',
  css: {
	'.sIFR-root': { 'color': '#ffffff' }
  },
  filters: {
	DropShadow: {
	   distance: 1
	  ,color: '#000000'
	  ,strength: 1
	  ,alpha: 0.5
	  ,angle: 30
	  ,knockout: false
	}
  }
});

sIFR.replace(gotham02, {
  selector: 'h2.success',
  wmode: 'transparent',
  css: {
	'.sIFR-root': { 'color': '#ffffff' },
	'strong': {'color': '#ffffff'}
  },
  filters: {
	DropShadow: {
	   distance: 1
	  ,color: '#000000'
	  ,strength: 1
	  ,alpha: 0.5
	  ,angle: 30
	  ,knockout: false
	}
  }
});

sIFR.replace(gotham02, {
  selector: 'h2.customize',
  wmode: 'transparent',
  css: {
	'.sIFR-root': { 'color': '#ffffff' }
  },
  filters: {
	DropShadow: {
	   distance: 1
	  ,color: '#000000'
	  ,strength: 1
	  ,alpha: 0.5
	  ,angle: 30
	  ,knockout: false
	}
  }
});

sIFR.replace(gotham08, {
  selector: 'div.large',
  wmode: 'transparent',
  css: {
    '.sIFR-root': { 'color': '#ffffff' }
  },
  filters: {
    DropShadow: {
       distance: 1
      ,color: '#000000'
      ,strength: 1
      ,alpha: 0.5
      ,angle: 30
      ,knockout: false
    }
  }
});

sIFR.replace(gotham08, {
  selector: 'div.small',
  wmode: 'transparent',
  css: {
    '.sIFR-root': { 'color': '#ffffff' }
  },
  filters: {
    DropShadow: {
       distance: 1
      ,color: '#000000'
      ,strength: 1
      ,alpha: 0.5
      ,angle: 30
      ,knockout: false
    }
  }
});

sIFR.replace(gotham04, {
  selector: 'h3.next',
  wmode: 'transparent',
  css: {
	'.sIFR-root': { 'color': '#ffffff' }
  }
});