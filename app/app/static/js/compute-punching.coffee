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
            $punchingError = $('.js-compute-punching-error')
            $punchingError.html('')
            $punchingResults = $('.js-results')
            $punchingResults.html('')
            $vrdc = $('.js-vrdc')
            $vrdmax = $('.js-vrdmax')
            $vrdc.val('')
            $vrdmax.val('')
            if data.success == true
                for info in data.info
                    $punchingResults.append('<br>' + info)
                $('.form-result2').html('Nośność na przebicie spełniona')
                $vrdc.val(data.vrdc)
                $vrdmax.val(data.vrdmax)
            if data.success == false
                if data.punching_errors
                    for error in data.punching_errors
                        $punchingError.append(error)
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


$ ->
    main()
