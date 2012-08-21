

ecochecks = new function() {
    this.debug = false,
    
    this.log = function(msg) {
        if (!this.debug) return;
        if(!this.browser.safari && window.console && console.log) console.log(msg);
        else alert(msg);
      }
      
      // THanks to: http://stackoverflow.com/questions/454875/how-to-do-browser-detection-with-jquery-1-3-with-browser-msie-deprecated/581065#581065
      var userAgent = navigator.userAgent.toLowerCase();
      this.browser = {
              version: (userAgent.match( /.+(?:rv|it|ra|ie)[\/: ]([\d.]+)/ ) || [0,'0'])[1],
              safari: /webkit/.test( userAgent ),
              opera: /opera/.test( userAgent ),
              msie: /msie/.test( userAgent ) && !/opera/.test( userAgent ),
              mozilla: /mozilla/.test( userAgent ) && !/(compatible|webkit)/.test( userAgent )
      };
      
      this.fade_errors_and_messages = function() {
          console.log("fade errors and stuff");
          $(".error").animate({opacity: 1.0}, 5000)
            .fadeOut();
      };
};

// Custom form replacement 
function form_replacement(default_values)
{
    this.default_values = default_values;
    
    this.fields = {};
    
    this.init = function()
    {
        this.prepare_fields();
    };
    
    this.prepare_fields = function()
    {
        ecochecks.log("preparing fields");
        var parent = this;
        for (var key in this.default_values)
        {
            ecochecks.log(">>" + key);
            var default_value = this.default_values[key]
            var jq_field = $("#id_" + key)
            var field = jq_field[0];
            
            this.fields[key] = { 'field' : field, 
                'default_value' : default_value,
                'has_custom' : field.value.length != 0 && field.value != default_value };
                        
            // set on click behavior, and blur behaviour for fields
            jq_field.blur(function() { parent.blur_field(key) });
            
            jq_field.focus(function() { parent.focus_field(key) });
        }
        
        this.reset_fields();
    };
    
    this.blur_field = function(key)
    {
        var field_data = this.fields[key];
        var field = field_data['field'];
        ecochecks.log("Blur field: " + field);
        
        if (field.value.length == 0) {
            var default_value = field_data['default_value'];
            ecochecks.log("\tsetting to " + default_value);
            field.value = default_value;
            this.fields[key]['has_custom'] = false;
        } else {
            this.fields[key]['has_custom'] = true;
        }
    };
    
    this.focus_field = function(key)
    {
        var field_data = this.fields[key];
        if (!field_data['has_custom']) {
            field_data['field'].value = "";
        }
    };
    
    this._has_custom_value = function(data) {

        if (!data['has_custom'] 
            || data['field'].value == data['default_value'] 
            || data['field'].value.length == 0) {
            return false;
        }
        
        return true;
    };
    
    this.reset_fields = function()
    {
        for (var k in this.fields) 
        {
            var data = this.fields[k];
            ecochecks.log("reset fields " + k)
            if (this._has_custom_value(data)) {
                ecochecks.log("\tdata has custom value");
                continue;
            }
            
            ecochecks.log("setting to default value ?");
            data['field'].value = data['default_value'];
        }
    };
    
    this.clear_defaults = function() 
    {
        for (var k in this.fields) {
            var data = this.fields[k];

            if (!this._has_custom_value(data)) {

                data['field'].value = "";
                ecochecks.log("new value? " + data['field'].value)
            }
        }
    }
    
    this.init();
};



