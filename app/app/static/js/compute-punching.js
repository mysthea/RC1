// Generated by CoffeeScript 1.9.3
(function() {
  var changeOptions, computePunching, main;

  computePunching = function() {
    return $.ajax({
      url: "/api/compute_punching",
      dataType: "json",
      type: "POST",
      data: {
        c_class: $('#id_c_class').val(),
        s_class: $('#id_s_class').val(),
        dsw: $('#id_dsw').val(),
        support: $('#id_support').val(),
        section: $('#id_section').val(),
        b: $('#id_b').val(),
        h: $('#id_h').val(),
        dx: $('#id_dx').val(),
        dy: $('#id_dy').val(),
        lx: $('#id_lx').val(),
        ly: $('#id_ly').val(),
        ad: $('#id_ad').val(),
        lambda_u: $('#id_lambda_u').val(),
        asx: $('#id_asx').val(),
        asy: $('#id_asy').val(),
        design_situation: $('#id_design_situation').val(),
        ved: $('#id_ved').val(),
        beta: $('#id_beta').val(),
        csrfmiddlewaretoken: $.cookie('csrftoken')
      },
      success: function(data, textStatus, jqXHR) {
        var $punchingResults, $resultInfo, $vrdc, $vrdmax, error, i, info, j, len, len1, ref, ref1;
        $punchingResults = $('.js-results');
        $punchingResults.html('');
        $vrdc = $('.js-vrdc');
        $vrdmax = $('.js-vrdmax');
        $vrdc.val('');
        $vrdmax.val('');
        $resultInfo = $('.form-result2');
        if (data.success === true) {
          ref = data.info;
          for (i = 0, len = ref.length; i < len; i++) {
            info = ref[i];
            $punchingResults.append('<br>' + info);
          }
          $resultInfo.html('Nośność na przebicie spełniona.');
          $vrdc.val(data.vrdc);
          $vrdmax.val(data.vrdmax);
        }
        if (data.success === false) {
          if (data.punching_errors) {
            ref1 = data.punching_errors;
            for (j = 0, len1 = ref1.length; j < len1; j++) {
              error = ref1[j];
              $punchingResults.append('<br>' + error);
            }
          }
          return $resultInfo.html('');
        }
      },
      error: function(jqXHR, textStatus, errorThrown) {
        return $('.js-compute-punching-error').html("Wystąpił nieoczekiwany błąd o kodzie " + jqXHR.status);
      }
    });
  };

  changeOptions = function() {
    var $betaInput, $lxInput, $lyInput, supportSelectedText;
    $lxInput = $('#id_lx');
    $lyInput = $('#id_ly');
    $betaInput = $('#id_beta');
    supportSelectedText = $('#id_support>option:selected').text();
    if (supportSelectedText === 'słup wewnętrzny') {
      $lxInput.prop('disabled', true);
      $lyInput.prop('disabled', true);
      return $betaInput.val(1.15);
    } else if (supportSelectedText === 'słup krawędziowy X') {
      $lxInput.prop('disabled', false);
      $lyInput.prop('disabled', true);
      return $betaInput.val(1.40);
    } else if (supportSelectedText === 'słup krawędziowy Y') {
      $lxInput.prop('disabled', true);
      $lyInput.prop('disabled', false);
      return $betaInput.val(1.40);
    } else if (supportSelectedText === 'słup narożny') {
      $lxInput.prop('disabled', false);
      $lyInput.prop('disabled', false);
      return $betaInput.val(1.50);
    } else {
      $lxInput.prop('disabled', true);
      $lyInput.prop('disabled', true);
      $('#id_support').val(1);
      return alert('Opcja w opracowaniu.');
    }
  };

  main = function() {
    var $supportSelect;
    $('.js-compute-punching').click(function(ev) {
      return computePunching();
    });
    changeOptions();
    $supportSelect = $('#id_support');
    return $supportSelect.on('change', function() {
      return changeOptions();
    });
  };

  $(function() {
    return main();
  });

}).call(this);
