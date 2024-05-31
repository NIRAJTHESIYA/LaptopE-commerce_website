$(document).ready(function () {
    $(window).on('load', function () {
        var charges = $('.charges').text();
        var grandTotal1 = $('.grandTotal2').text();
        var gTotal = 0
        gTotal = parseInt(charges) + parseInt(grandTotal1)
        $('.grandTotal2').html(gTotal)
    });

    $('#aread').change(function (e) { 
        e.preventDefault();
        
        var charges = $('.charges').text();
        var grandTotal1 = $('.grandTotal2').text();
        var area = $(this).val();
        var gTotal
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/change-charges",
            data: {
                'delivery_charges':charges,
                'areaname':area,
                csrfmiddlewaretoken:token
            },
            success: function (response) {
                $('.charges').html(response.status)
                gTotal = (parseInt(grandTotal1) - parseInt(charges))
                gTotal1 = gTotal + parseInt(response.status)
                $('.grandTotal2').html(gTotal1)
            }
        });
    });
});