computePunching = ->
    $.ajax({
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
        success: (data, textStatus, jqXHR) ->
            $punchingResults = $('.js-results')
            $punchingResults.html('')
            $vrdc = $('.js-vrdc')
            $vrdmax = $('.js-vrdmax')
            $vrdc.val('')
            $vrdmax.val('')
            $resultInfo = $('.form-result2')
            if data.success == true
                for info in data.info
                    $punchingResults.append('<br>' + info)
                $resultInfo.html('Nośność na przebicie spełniona.')
                $vrdc.val(data.vrdc)
                $vrdmax.val(data.vrdmax)
            if data.success == false
                if data.punching_errors
                    for error in data.punching_errors
                        $punchingResults.append('<br>' + error)
                $resultInfo.html('')
                # TODO: zastanowić się, które pola formularza mogą rzucić błędem walidacji, dodać im odpowiednie spany w punching.html i uzupełnić poniższe
#                if data.errors
#                    errorDict = {
#                        'c_class': $('.js-c_class-error'),
#                    }
#                    for k, v of errorDict
#                        if data.errors[k]
#                            v.html(data.errors[k])
#                        else
#                            v.html('')
        error: (jqXHR, textStatus, errorThrown) ->
            $('.js-compute-punching-error').html("Wystąpił nieoczekiwany błąd o kodzie #{jqXHR.status}")
    })


main = ->
    $('.js-compute-punching').click (ev) ->
        computePunching()

    $supportSelect = $('#id_support')
    $lxInput = $('#id_lx')
    $lyInput = $('#id_ly')
    $betaInput = $('#id_beta')
    $supportSelect.on('change', ->
        supportSelectedText = $('#id_support>option:selected').text()
        if supportSelectedText == 'słup wewnętrzny'
            $lxInput.prop('disabled', true)
            $lyInput.prop('disabled', true)
            $betaInput.val(1.15)            
        else if supportSelectedText == 'słup krawędziowy X'
            $lxInput.prop('disabled', false)
            $lyInput.prop('disabled', true)
            $betaInput.val(1.40)
        else if supportSelectedText == 'słup krawędziowy Y'
            $lxInput.prop('disabled', true)
            $lyInput.prop('disabled', false)
            $betaInput.val(1.40)
        else if supportSelectedText == 'słup narożny'
            $lxInput.prop('disabled', false)
            $lyInput.prop('disabled', false)
            $betaInput.val(1.50)
        else
            $lxInput.prop('disabled', true)
            $lyInput.prop('disabled', true)
            $supportSelect.val(1)
            alert 'Opcja w opracowaniu.'
    )


$ ->
    main()
