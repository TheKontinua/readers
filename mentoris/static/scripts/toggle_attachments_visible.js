/*
* A method to toggle the visibility of attachments
* list_element_id   The container that the attachments and button are in
* button   The reference to the button in the attachments container
* attachment_class_name   The name of the class that contains the attachments to show or hide
*
* Assumes that the button has the class visible_state to indicate it is currently visible
*/
function toggle_attachments_visible(list_element_id, button, attachment_class_name){
    var list_element = document.getElementById(list_element_id);
    var list = list_element.children;
    var index = -1;

    for(var i = 0; i < list.length; ++i){
        if(list[i].contains(button)){
            index = i;
        }
    }
    if(index != -1){
        if($(button).hasClass("visible_state")){
            $(button).text("Show Attachments");
            $(button).addClass("invisible_state");
            $(list[index].getElementsByClassName(attachment_class_name)[0]).hide();
            $(button).removeClass("visible_state");

        } else {
            $(button).text("Hide Attachments");
            $(button).addClass("visible_state");
            $(list[index].getElementsByClassName(attachment_class_name)[0]).show();
            $(button).removeClass("invisible_state");
        }
    }
}