var app = angular.module("pharlap", ['lens.bridge', 'lens.ui']);

function PharlapCtrl($scope, $modal) {
  $scope.curtain = {
    progress: 0,
    message: 'Reading repository information ...'
  };

  $scope.types = ['input', 'graphics', 'network', 'sound', 'other'];

  $scope.data = {
    devices: {},
    modules: {},
    loaded_modules: {},
    modaliases: {},
  };

  $scope.settings = {
    show_akmods: true,
    show_kmods: false,
    blacklist_other: true
  };

  $scope.system = {
    arch:       '64-bit (x64_64)',
    distribution: {
      name:     'Korora',
      codename: 'Peach',
      desktop:  'GNOME',
      version:  '20',
      live:     true,
    },
    memory: {
      total:      8080964,
      free:       256456,
      available:  2477224,
      buffers:    264148,
      cached:     2207288,
      swapCached: 24248,
      swapTotal:  8142844,
      swapFree:   7535684
    },
    cpu: {
      model: 'Intel(R) Core(TM) i7-3520M CPU @ 2.90GHz',
      sockets: 1,
      cores_per_sockets: 2,
      threads_per_core: 2,
      clock:    3577.648,
      clockMax: 3600.0000,
      clockMin: 1200.0000
    },
    current_kernel: ''
  };

  $scope.openModuleSettingsModal = function(name, settings) {

    var modalInstance = $modal.open({
      backdrop: 'static',
      controller: PharlapModuleSettingsModalCtrl,
      size: 'lg',
      templateUrl: 'moduleSettingsModal.html',
      resolve: {
        data: function() {
          return {
            name: name,
            settings: angular.copy(settings)
          };
        }
      }
    });

    modalInstance.result.then(function(data) {
      if( data.hasOwnProperty('name') &&
          data.hasOwnProperty('settings') ) {
        $scope.data.modules[data.name] = data.settings;

        /* update module information */
        $scope.processDevices();
      }
    });
  };

  $scope.openModuleSettings = function(name) {
    var settings = {};
    if( $scope.data.modules.hasOwnProperty(name) ) {
      settings = $scope.data.modules[name];
    }

    $scope.openModuleSettingsModal(name, settings);
  };

  $scope.countDeviceByClass = function(filter) {
    var result = 0;

    angular.forEach($scope.data.devices, function(v, k) {
      if( v.hasOwnProperty('class') && v['class'] === filter ) {
        result++
      }
    });

    return result > 0 ? result : '';
  };

  $scope.filterDeviceByClass = function(filter) {
    var result = {};

    angular.forEach($scope.data.devices, function(v, k) {
      if( v.hasOwnProperty('class') && v['class'] === filter ) {
        result[k] = v;
      }
    });

    return result;
  };

  $scope.filterDrivers = function(drivers) {
    var result = {};
    var _kernel = '-' + $scope.system.current_kernel;

    angular.forEach(drivers, function(v, k) {
      /* process akmods */
      if( k.indexOf('akmod') === 0 ) {
        if( $scope.settings.show_akmods ) {
          result[k] = v;
        }
      }
      /* process kmods */
      else if( (k.indexOf('kmod') === 0) ) {
        if( $scope.settings.show_kmods && k.indexOf(_kernel) > 0 ) {
          result[k] = v;
        }
      }
      /* process everything else */
      else {
        result[k] = v;
      }
    });

    return result;
  };

  $scope.selectDriver = function(device, driver) {
    for(var d in device.drivers) {
      if( d === driver) {
        device.drivers[d].selected = true;
      }
      else {
        delete device.drivers[d].selected;
      }
    }
  };

  $scope.isSelected = function(driver) {
    return driver.hasOwnProperty('selected') && driver.selected;
  };

  $scope.isRecommended = function(driver) {
    return driver.hasOwnProperty('free') && driver.free &&
           driver.hasOwnProperty('from_distro') && driver.from_distro;
  };

  $scope.getIconName = function(e) {
    return 'logo-' + e.toLowerCase().replace(/ /, '-') + '.png';
  };

  $scope.driverHasModules = function(dv) {
    return dv.hasOwnProperty('modules') && Object.keys(dv.modules).length > 0;
  };

  $scope.isLoaded = function(pv, m) {
    return pv.hasOwnProperty('loaded') && pv.loaded.indexOf(m) !== -1;
  };

  $scope.isBlacklisted = function(name) {
    modules = $scope.data.modules;
    return modules.hasOwnProperty(name) && modules[name].blacklisted;
  };

  $scope.getQuirks = function(module) {
    modules = $scope.data.modules;
    return modules.hasOwnProperty(name) ? modules[name].options : '';
  };

  $scope.hasQuirks = function(module) {
    modules = $scope.data.modules;
    return modules.hasOwnProperty(name) && modules[name].options.length > 0;
  };

  $scope.processDevices = function() {
    angular.forEach($scope.data.devices, function(v, k) {

      /* decorate with loaded */
      if( $scope.data.loaded_modules.hasOwnProperty(v.modalias) ) {
        v.loaded = $scope.data.loaded_modules[v.modalias].module;
      }

      /* decorate with module information */
      if( v.hasOwnProperty('drivers') && v.hasOwnProperty('loaded') ) {
        angular.forEach(v.drivers, function(dv, dk) {
          /* driver is selected if it contains the module that's loaded */
          if( dv.hasOwnProperty('modules') && v.loaded.length > 0 ) {
            for( var _i=0, _l=v.loaded.length; _i<_l; _i++ ) {
              if( dv.modules.indexOf(v.loaded[_i]) !== -1 ) {
                dv.selected = true;
                break;
              }
            }
          }
        });
      }
    });
  };

  $scope.hasChanges = function() {
    _m = angular.equals($scope.data._modules, $scope.data.modules);
    _d = angular.equals($scope.data._devices, $scope.data.devices);

    console.log($scope.data._devices, $scope.data.devices);

    return  _m && _d;
  };

  $scope.revertChanges = function() {
    /* restore original configuration */
    $scope.data.modules = angular.copy($scope.data._modules);
    $scope.data.devices = angular.copy($scope.data._devices);
  };

  /* SIGNALS */

  // register to configuration updates
  $scope.$on('update-progress', function(e, progress, message) {
    $scope.curtain.progress = progress;
    $scope.curtain.message = "Searching for packages that match your hardware ...";
  });

  // register for appLoaded state
  $scope.$on('init-complete', function(e) {
    $('.page-container').removeClass('hide');
    $('.curtain').fadeOut('slow');
  });


  $scope.$on('init-config', function(e, k, ma, lm, d, m) {
    $scope.system.current_kernel = k;
    $scope.data.loaded_modules = lm;
    $scope.data.devices = d;
    $scope.data.modules = m;

    $scope.processDevices();

    $scope.data._modules = angular.copy($scope.data.modules);
    $scope.data._devices = angular.copy($scope.data.devices);
  });

  // INIT
  $scope.emit("init");
}

var PharlapModuleSettingsModalCtrl = function($scope, $modalInstance, data) {
  $scope.data = data;

  $scope.ok = function() {
    $modalInstance.close($scope.data);
  };

  $scope.cancel = function() {
    $modalInstance.dismiss('cancel');
  };
};

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

  $(".dial").knob({
    readOnly: true,
    width: 100,
    angleOffset: -125,
    angleArc: 250
  });

  /* initial call to page resize helper */
  setTimeout(function() { resizeHelper(); $('.loader').fadeIn('slow')}, 0);

  /* TODO: fake slow load */
  //setTimeout(function() { angular.element(document).scope().$broadcast('appLoaded'); }, 3000);
});
