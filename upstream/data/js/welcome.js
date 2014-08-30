/*
** ANGULAR DEFINITIONS
*/
var app = angular.module("pharlap", []);
//var app_rscope = angular.injector(['ng']).get('$rootScope');
var app_rs;

app.directive('module-active-badge', function() {
  return {
    restrict: 'E',
    scope: {
      details: '=details'
    },
    template: '<span class="badge">ACTIVE</span>'
  };
});

function PharlapCtrl($scope) {
  $scope.config = {
    arch:       'n/a',
    codename:   'n/a',
    desktop:    'n/a',
    version:    'n/a',
    live:       true,
    auto_start: false,
  };

  $scope.devices = {
    "/sys/devices/pci0000:00/0000:00:1b.0":{
      "loaded":"snd_hda_intel",
      "vendor":"Intel Corporation",
      "model":"7 Series/C210 Series Chipset Family High Definition Audio Controller",
      "modalias":"pci:v00008086d00001E20sv00008086sd00007270bc04sc03i00",
      "drivers":{
        "kernel":{
          "version":"3.15.10",
          "modules":{
            "snd-hda-intel":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":true,
          "free":false,
          "summary":"The Linux kernel"
        }
      },
      "class":"sound"
    },
    "/sys/devices/pci0000:00/0000:00:1c.1/0000:02:00.0":{
      "loaded":"bcma",
      "vendor":"Broadcom Corporation",
      "model":"BCM4331 802.11a/b/g/n",
      "modalias":"pci:v000014E4d00004331sv0000106Bsd000000F5bc02sc80i00",
      "drivers":{
        "kmod-wl-3.13.4-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.13.4-200.fc20.x86_64"
        },
        "kernel":{
          "version":"3.15.10",
          "modules":{
            "bcma":{
              "loaded":false,
              "quirks":"host=0",
              "blacklisted":true
            }
          },
          "from_distro":true,
          "free":false,
          "summary":"The Linux kernel"
        },
        "kmod-wl-3.12.6-300.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":true
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.12.6-300.fc20.x86_64"
        },
        "kmod-wl-3.12.7-300.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.12.7-300.fc20.x86_64"
        },
        "kmod-wl-3.12.10-300.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.12.10-300.fc20.x86_64"
        },
        "kmod-wl-3.13.9-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.13.9-200.fc20.x86_64"
        },
        "kmod-wl-3.14.9-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.14.9-200.fc20.x86_64"
        },
        "kmod-wl-3.14.4-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.14.4-200.fc20.x86_64"
        },
        "kmod-wl-3.12.9-301.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.12.9-301.fc20.x86_64"
        },
        "kmod-wl-3.13.7-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.13.7-200.fc20.x86_64"
        },
        "kmod-wl-3.12.8-300.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.12.8-300.fc20.x86_64"
        },
        "kmod-wl-3.15.5-200.fc20.x86_64":{
          "version":"6.30.223.248",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.15.5-200.fc20.x86_64"
        },
        "kmod-wl-3.14.1-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.14.1-200.fc20.x86_64"
        },
        "kmod-wl-3.14.8-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.14.8-200.fc20.x86_64"
        },
        "kmod-wl-3.13.8-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.13.8-200.fc20.x86_64"
        },
        "kmod-wl-3.15.7-200.fc20.x86_64":{
          "version":"6.30.223.248",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.15.7-200.fc20.x86_64"
        },
        "kmod-wl-3.11.10-301.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted": true
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.11.10-301.fc20.x86_64"
        },
        "kmod-wl-3.14.5-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.14.5-200.fc20.x86_64"
        },
        "kmod-wl-3.13.10-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.13.10-200.fc20.x86_64"
        },
        "kmod-wl-3.13.5-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.13.5-200.fc20.x86_64"
        },
        "kmod-wl-3.15.8-200.fc20.x86_64":{
          "version":"6.30.223.248",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.15.8-200.fc20.x86_64"
        },
        "kmod-wl-3.14.7-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.14.7-200.fc20.x86_64"
        },
        "kmod-wl-3.13.3-201.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.13.3-201.fc20.x86_64"
        },
        "kmod-wl-3.14.6-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.14.6-200.fc20.x86_64"
        },
        "kmod-wl-3.15.6-200.fc20.x86_64":{
          "version":"6.30.223.248",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.15.6-200.fc20.x86_64"
        },
        "kmod-wl-3.14.2-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.14.2-200.fc20.x86_64"
        },
        "kmod-wl-3.12.5-302.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.12.5-302.fc20.x86_64"
        },
        "kmod-wl-3.15.10-200.fc20.x86_64":{
          "version":"6.30.223.248",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.15.10-200.fc20.x86_64"
        },
        "kmod-wl-3.14.3-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.14.3-200.fc20.x86_64"
        },
        "kmod-wl-3.13.6-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.13.6-200.fc20.x86_64"
        },
        "kmod-wl-3.15.9-200.fc20.x86_64":{
          "version":"6.30.223.248",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.15.9-200.fc20.x86_64"
        },
        "kmod-wl-3.15.4-200.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.15.4-200.fc20.x86_64"
        },
        "kmod-wl-3.12.9-300.fc20.x86_64":{
          "version":"6.30.223.141",
          "modules":{
            "wl":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":false,
          "free":false,
          "summary":"wl kernel module(s) for 3.12.9-300.fc20.x86_64"
        }
      },
      "class":"network"
    },
    "/sys/devices/pci0000:00/0000:00:1c.2/0000:03:00.0":{
      "loaded":"firewire_ohci",
      "vendor":"LSI Corporation",
      "model":"FW643 [TrueFire] PCIe 1394b Controller",
      "modalias":"pci:v000011C1d00005901sv000011C1sd00005900bc0Csc00i10",
      "drivers":{
        "kernel":{
          "version":"3.15.10",
          "modules":{
            "firewire-ohci":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":true,
          "free":false,
          "summary":"The Linux kernel"
        }
      },
      "class":"other"
    },
    "/sys/devices/pci0000:00/0000:00:1f.3":{
      "loaded":null,
      "vendor":"Intel Corporation",
      "model":"7 Series/C210 Series Chipset Family SMBus Controller",
      "modalias":"pci:v00008086d00001E22sv00008086sd00007270bc0Csc05i00",
      "drivers":{
        "kernel":{
          "version":"3.15.10",
          "modules":{
            "i2c-i801":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":true,
          "free":false,
          "summary":"The Linux kernel"
        }
      },
      "class":"other"
    },
    "/sys/devices/pci0000:00/0000:00:1c.0/0000:01:00.1":{
      "loaded":"sdhci_pci",
      "vendor":"Broadcom Corporation",
      "model":"BCM57765/57785 SDXC/MMC Card Reader",
      "modalias":"pci:v000014E4d000016BCsv000014E4sd00000000bc08sc05i01",
      "drivers":{
        "kernel":{
          "version":"3.15.10",
          "modules":{
            "sdhci-pci":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":true,
          "free":false,
          "summary":"The Linux kernel"
        }
      },
      "class":"other"
    },
    "/sys/devices/pci0000:00/0000:00:1c.0/0000:01:00.0":{
      "loaded":"tg3",
      "vendor":"Broadcom Corporation",
      "model":"NetXtreme BCM57765 Gigabit Ethernet PCIe",
      "modalias":"pci:v000014E4d000016B4sv000014E4sd000016B4bc02sc00i00",
      "drivers":{
        "kernel":{
          "version":"3.15.10",
          "modules":{
            "tg3":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":true,
          "free":false,
          "summary":"The Linux kernel"
        }
      },
      "class":"network"
    },
    "/sys/devices/pci0000:00/0000:00:16.0":{
      "loaded":"mei_me",
      "vendor":"Intel Corporation",
      "model":"7 Series/C210 Series Chipset Family MEI Controller #1",
      "modalias":"pci:v00008086d00001E3Asv00008086sd00007270bc07sc80i00",
      "drivers":{
        "kernel":{
          "version":"3.15.10",
          "modules":{
            "mei-me":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":true,
          "free":false,
          "summary":"The Linux kernel"
        }
      },
      "class":"other"
    },
    "/sys/devices/pci0000:00/0000:00:02.0":{
      "loaded":"drm",
      "vendor":"Intel Corporation",
      "model":"3rd Gen Core processor Graphics Controller",
      "modalias":"pci:v00008086d00000166sv0000106Bsd000000FAbc03sc00i00",
      "drivers":{
        "kernel":{
          "version":"3.15.10",
          "modules":{
            "i915":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":true,
          "free":false,
          "summary":"The Linux kernel"
        }
      },
      "class":"graphics"
    },
    "/sys/devices/pci0000:00/0000:00:1f.0":{
      "loaded":"lpc_ich",
      "vendor":"Intel Corporation",
      "model":"HM77 Express Chipset LPC Controller",
      "modalias":"pci:v00008086d00001E57sv00008086sd00007270bc06sc01i00",
      "drivers":{
        "kernel":{
          "version":"3.15.10",
          "modules":{
            "lpc_ich":{
              "loaded":false,
              "quirks":"",
              "blacklisted":false
            }
          },
          "from_distro":true,
          "free":false,
          "summary":"The Linux kernel"
        }
      },
      "class":"other"
    }
  };

  $scope.driverHasModules = function(dv) {
    return dv.hasOwnProperty('modules') && Object.keys(dv.modules).length > 0;
  };

  $scope.getModuleLoadedLabel = function(pv, m) {
    return ( pv.hasOwnProperty('loaded') && pv.loaded === m ) ? 'Loaded' : '';
  };

  $scope.getModuleBlacklistedLabel = function(mv) {
    return ( mv.hasOwnProperty('blacklisted') && mv.blacklisted ) ? 'Blacklisted' : '';
  };

  $scope.formatHideZero = function(c) {
    return c > 0 ? c : "";
  };

  $scope.hasQuirks = function(mv) {
    return mv.hasOwnProperty('quirks') && mv.quirks.length > 0;
  };

  $scope.countDeviceByClass = function(c) {
    var count = 0;

    angular.forEach($scope.devices, function(v, k) {
      if( v.hasOwnProperty('class') && v['class'] == c ) {
        count++;
      }
    });

    return count;
  };

  $scope.filterDeviceByClass = function(c) {
    var result = {};

    angular.forEach($scope.devices, function(v, k) {
      if( v.hasOwnProperty('class') && v['class'] == c ) {
        result[k] = v;
      }
    });

    return result;
  };

  $scope.selectDriver = function(device, driver) {
    console.log(device);

    for(var d in device.drivers) {
      device.drivers[d].selected = ( d === driver );
    }
  };

  $scope.isSelected = function(driver) {
    return driver.hasOwnProperty('selected') && driver.selected;
  };

  $scope.isRecommended = function(driver) {
    return driver.hasOwnProperty('free') && driver.free &&
           driver.hasOwnProperty('from_distro') && driver.from_distro;
  };

  $scope.getRecommendation = function(driver) {
    return $scope.isRecommended(driver) ? "recommended" : "";
  };

  $scope.getIconName = function(e) {
    return 'logo-' + e.toLowerCase().replace(/ /, '-') + '.png';
  };

  // call the python-webkit bridge
  $scope.emitPYTHON = function() {
    var _args = Array.prototype.slice.call(arguments);

    if( _args.length > 0 ) {
      var _command = {
        "signal": _args.shift(),
        "message": _args
      }

      /* update document title */
      document.title = '_BR::' + angular.toJson(_command, false);
    }
  }

  // register to configuration updates
  $scope.$on('configUpdate', function(e, k, v) {
    $scope[k] = v;
    console.log('config update: ' + k);
  });


  // register for appLoaded state
  $scope.$on('appLoaded', function(e) {
    console.log('app loaded');

    $('.page-container').removeClass('hide');
    $('.curtain').fadeOut('slow');
  });

  // INIT
  $scope.emitPYTHON("post_init");
}

/*
** PAGE HANDLER
*/
$(document).ready( function() {
  /* configure korobar */
  var fixed   = true;
  var korobar = $('#korobar');
  var page    = $('.page-container');
  var footer  = $('footer');
  var start   = 0;

  /* helper function to frob element heights for the layered effect */
  var resizeHelper = function() {
    // banner correction
    if( $('#banner').length ) {
      start = $('#banner').outerHeight();
    }

    /* calculate korobar position and initial pinning state */
    if( start - $(window).scrollTop() <= 0 ) {
      korobar.css({ position: 'fixed', top: 0 });
      fixed = true;
    }
    else {
      korobar.css({ position: 'absolute', top: start + 'px' });
      fixed = false;
    }

    /* frob page-container minimum height to at least the footer top */
    page.css({
      'min-height': ($(window).height()-footer.outerHeight()) + 'px',
      'margin-bottom': footer.outerHeight() + 'px'
    });

    /* frob page-content minimum height to consume immediate window */
    $('.page-content').css('min-height', ( $(window).height() - 96 )  + 'px');
  }

  /* pin korobar to top when it passes */
  $(window).on('scroll', function() {
    if( !fixed && (korobar.offset().top - $(window).scrollTop() <= 0) ) {
      korobar.css({ position: 'fixed', top: 0, });
      fixed = true;
    }
    else if( fixed && $(window).scrollTop() <= start ) {
      korobar.css({ position: 'absolute', top: start + 'px' });
      fixed = false;
    }
  });

  /* bind to resize events */
  $(window).on('resize', resizeHelper);

  /* turn on tooltips */
  $("[data-toggle='tooltip']").tooltip();

  /* turn on tabs */
  $("[data-toggle='tab']").on('click', function(e) {
    e.preventDefault();
    $(this).tab('show');
  });

  /* smooth scroll targets */
  $('a[href*=#]:not([href=#]):not([data-toggle])').click(function() {
    if( location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') || location.hostname == this.hostname ) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if( target.length ) {
        $('html,body').animate({ scrollTop: target.offset().top - korobar.height() - 16 }, 1000);
        return false;
      }
    }
  });

  /* initial call to page resize helper */
  setTimeout(function() { resizeHelper(); $('.loader').fadeIn('slow')}, 0);


  /* fetch the rootscope */
  app_rs = angular.element(document).scope();

  /* TODO: fake slow load */
  /*setTimeout(function() { app_rs.$broadcast('appLoaded'); }, 5000); */
});


