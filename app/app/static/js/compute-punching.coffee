computePunching = ->
    cClass = $('#id_c_class').val()
    sClass = $('#id_s_class').val()
    dsw = $('#id_dsw').val()
    support = $('#id_support').val()
    section = $('#id_section').val()
    b = $('#id_b').val()
    h = $('#id_h').val()
    dx = $('#id_dx').val()
    dy = $('#id_dy').val()
    lx = $('#id_lx').val()
    ly = $('#id_ly').val()
    ad = $('#id_ad').val()
    lambdaU = $('#id_lambda_u').val()
    asx = $('#id_asx').val()
    asy = $('#id_asy').val()
    design_situation = $('#id_design_situation').val()
    ved = $('#id_ved').val()
    beta = $('#id_beta').val()

    $.ajax({
        url: "/api/compute_punching",
        dataType: "json",
        type: "POST",
        data: {
            c_class: cClass,
            s_class: sClass,
            dsw: dsw,
            support: support,
            section: section,
            b: b,
            h: h,
            dx: dx,
            dy: dy,
            lx: lx,
            ly: ly,
            ad: ad,
            lambda_u: lambdaU,
            asx: asx,
            asy: asy,
            design_situation: design_situation,
            ved: ved,
            beta: beta,
            csrfmiddlewaretoken: $.cookie('csrftoken')
        },
        success: (data, textStatus, jqXHR) ->
            $punchingError = $('.js-compute-punching-error')
            $punchingError.html('')
            $vrdc = $('.js-vrdc')
            $vrdmax = $('.js-vrdmax')
            $vrdc.val('')
            $vrdmax.val('')
            if data.success == true
                $vrdc.val(data.vrdc)
                $vrdmax.val(data.vrdmax)
                console.log('Hura')
            if data.success == false
                console.log('Buuuuuu')
                if data.punching_errors
                    for error in data.punching_errors
                        $punchingError.append(error)
                    # TODO
    #           if data.errors
    #                errorDict = {
    #                    'c_class': $('.js-c_class-error'),
    #                }
    #                if data.errors
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
