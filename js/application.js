jQuery.fn.outer = function(){
    return $($('<div></div>').html(this.clone())).html();
}

function showHint(element_id, text){
    $('#' + element_id).focus(function(){
        if ($(this).val() == text) {
            $(this).val('');
        }
    });

    $('#' + element_id).blur(function(){
        if ($(this).val() == '') {
            $(this).val(text);
        }
    });

    $('#' + element_id).blur();
}

function showPassHint(passelement_id, textelement_id){
    $('#' + textelement_id).show();
    $('#' + passelement_id).hide();

    $('#' + textelement_id).focus(function(){
    	$('#' + textelement_id).hide();
    	$('#' + passelement_id).show();
    	$('#' + passelement_id).focus();
    });
    $('#' + passelement_id).blur(function(){
        if ($('#' + passelement_id).val() == '') {
        	$('#' + textelement_id).show();
            $('#' + passelement_id).hide();
        }
    });
}

function showHostDomain(host_id,domain_id){
	host_val= $('#' + host_id).val();
	domain_val= $('#' + domain_id).val();

	$('#' + host_id).focus(function(){
        $(this).val('');
        $('#' + domain_id).val(domain_val)
    });
	
	
	$('#' + domain_id).focus(function(){
        $(this).val('');
        $('#' + host_id).val(host_val)
    });
}

