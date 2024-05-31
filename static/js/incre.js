$(document).ready(function () {
    $('.increment-btn').click(function (e) {
        e.preventDefault();

        var inc_value = $(this).closest('.pro_data').find('.qty-input').val();
        var value = parseInt(inc_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value < 10) {
            value++;
            $(this).closest('.pro_data').find('.qty-input').val(value);
        }
    });

    $('.decrement-btn').click(function (e) {
        e.preventDefault();

        var dec_value = $(this).closest('.pro_data').find('.qty-input').val();
        var value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1) {
            value--;
            $(this).closest('.pro_data').find('.qty-input').val(value);
        }
    });

    $('.AddToCartBtn').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.pro_data').find('.product_id').val();
        var product_qty = $(this).closest('.pro_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            type: 'POST',
            url: "/add-to-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.set('notifier', 'position', 'top-right');
                if (response.status) {
                    alertify.success(response.status);
                } else {
                    alertify.error(response.data);
                }
            }
        });
    });

    $('.AddToWishListBtn').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.pro_data').find('.product_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add-to-wishlist",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.set('notifier', 'position', 'top-right');
                if (response.status) {
                    alertify.success(response.status);
                } else {
                    alertify.error(response.data);
                }
            }
        });
    });

    $('.changeQuantity').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.pro_data').find('.product_id').val();
        var product_qty = $(this).closest('.pro_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            type: 'POST',
            url: "/change-quantity",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response.status)
            }
        });
    });

    $('.delete-cart-product').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.pro_data').find('.product_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "delete-cart-product",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token

            },
            success: function (response) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.success(response.status);
                $('.carddata').load(location.href + " .carddata")
            }
        });
    });

    $('.delete-wishlist-product').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.wishlistdata').find('.product_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/delete-wishlist-product",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.success(response.status);
                $('.wishlistdata').load(location.href + " .wishlistdata")
            }
        });
    });

    $('.delete-order').click(function (e) {
        e.preventDefault();

        let confirmation = confirm("Are you sure you want to cancel order?");

        var order_id = $(this).closest('.product_data').find('.order_tracking_no').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        if (confirmation) {
            $.ajax({
                method: "POST",
                url: "/cancelOrder",
                data: {
                    'order_id': order_id,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    alertify.set('notifier', 'position', 'top-right');
                    $('.card-data').load(location.href + " .card-data");
                    if (response.status) {
                        alertify.success(response.status);
                    } else {
                        alertify.error(response.data);
                    }
                }
            });
        }
    });

    
  
    // $('.changeQuantity_accessory').click(function (e) {
    //     e.preventDefault();

    //     var accessory_id = $(this).closest('.accepro_data').find('.acc_id').val();
    //     var accessory_qty = $(this).closest('.accepro_data').find('.qty-input').val();
    //     var token = $('input[name=csrfmiddlewaretoken]').val();

    //     $.ajax({
    //         type: 'POST',
    //         url: "/change-quantity_accessory",
    //         data: {
    //             'accessory_id': accessory_id,
    //             'accessory_qty': accessory_qty,
    //             csrfmiddlewaretoken: token
    //         },
    //         success: function (response) {
    //             console.log(response.status)
    //         }
    //     });
    // });

    // $('.delete-cart-accessory').click(function (e) {
    //     e.preventDefault();

    //     var accessory_id = $(this).closest('.accepro_data').find('.accessory_id').val();
    //     var token = $('input[name=csrfmiddlewaretoken]').val();

    //     $.ajax({
    //         method: "POST",
    //         url: "delete-cart-product",
    //         data: {
    //             'product_id': product_id,
    //             csrfmiddlewaretoken: token

    //         },
    //         success: function (response) {
    //             alertify.set('notifier', 'position', 'top-right');
    //             alertify.success(response.status);
    //             $('.carddata').load(location.href + " .carddata")
    //         }
    //     });
    // });
});


