jQuery(function() {
    initialiseCKEditor();
    initialiseCKEditorInInlinedForms();

    function initialiseCKEditorInInlinedForms() {
        jQuery(".add-row a, .grp-add-handler").click(function () {
            initialiseCKEditor();
            return true;
        });
    }
});

function initialiseCKEditor() {
    jQuery('textarea[data-type=ckeditortype]').each(function(){
        if(jQuery(this).data('processed') == "0" && jQuery(this).attr('id').indexOf('__prefix__') == -1){
            jQuery(this).data('processed',"1");
            CKEDITOR.replace(jQuery(this).attr('id'), jQuery(this).data('config'));
        }
    });
}