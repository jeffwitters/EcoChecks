/* 
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */


tinyMCE.init({ 
mode : "textareas",
theme :"advanced",
theme_advanced_toolbar_location :"top",
theme_advanced_toolbar_align : "left",
theme_advanced_buttons1 :"fullscreen,preview,separator,cut,copy,paste,separator,undo,redo,separator,bold,italic,underline,strikethrough,sub,sup,separator,bullist,numlist,outdent,indent,link,unlink,anchor,separator,image,cleanup",
theme_advanced_buttons2 : "formatselect,fontselect,fontsizeselect,separator,forecolor,backcolor,separator,help,separator,code",
theme_advanced_buttons3 :"",
auto_cleanup_word : true,
plugins :"table,advhr,advimage,advlink,preview,fullscreen",
plugin_insertdate_dateFormat :"%d/%m/%Y",
plugin_insertdate_timeFormat : "%H:%M:%S",
extended_valid_elements : "a[name|href|target=_blank|title|onclick],img[class|src|border=0|alt|title|hspace|vspace|width|height|align|onmouseover|onmouseout|name],hr[class|width|size|noshade],font[face|size|color|style],span[class|align|style]",
fullscreen_settings : {
theme_advanced_path_location : "top",
theme_advanced_buttons1 : "fullscreen,preview,separator,cut,copy,paste,separator,undo,redo,separator,bold,italic,underline,strikethrough,sub,sup,separator,bullist,numlist,outdent,indent,link,unlink,anchor,separator,image,cleanup",
theme_advanced_buttons2 : "formatselect,fontselect,fontsizeselect,separator,forecolor,backcolor,separator,help,separator,code",
theme_advanced_buttons3 : ""
}
});
