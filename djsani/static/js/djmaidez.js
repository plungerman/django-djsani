function GetUserType() {
    return "student";
}
function makeDialog() {
    $("#main_modal").dialog({
        autoOpen: true,
        height: 620,
        width: 850,
        modal: true,
        top: 10,
        buttons: { "Save": function(){
            if(isValid() && !isNaN(GetUserID())) {
                var subdomain = getSubdomain();
                var earl = "https://" + subdomain + ".carthage.edu/emergency/contact/save?uid="+GetUuid()+"&callback=?";
                $.getJSON(earl, {
                    MIS1_NAME: $("#MIS1_NAME").val(),
                    MIS1_REL: $("#MIS1_REL").val(),
                    MIS1_PHONE1: $("#MIS1_PHONE1").val(),
                    MIS1_PHONE2: $("#MIS1_PHONE2").val(),
                    MIS1_PHONE3: $("#MIS1_PHONE3").val(),
                    MIS2_NAME: $("#MIS2_NAME").val(),
                    MIS2_PHONE1: $("#MIS2_PHONE1").val(),
                    MIS3_NAME: $("#MIS3_NAME").val(),
                    MIS3_PHONE1: $("#MIS3_PHONE1").val(),
                    ENS_SELF_CELL: $("#ENS_SELF_CELL").val(),
                    ENS_SMS: "1",
                    ENS_CARRIER: $("#ENS_CARRIER").val(),
                    ENS_EMAIL: $("#ENS_EMAIL").val(),
                    ICE_NAME: $("#ICE_NAME").val(),
                    ICE_PHONE1: $("#ICE_PHONE1").val(),
                    ICE_PHONE2: $("#ICE_PHONE2").val(),
                    ICE_PHONE3: $("#ICE_PHONE3").val(),
                    ICE_REL: $("#ICE_REL").val(),
                    ICE2_NAME: $("#ICE2_NAME").val(),
                    UserID: GetUserID(),
                    ICE2_PHONE1: $("#ICE2_PHONE1").val(),
                    ICE2_PHONE2: $("#ICE2_PHONE2").val(),
                    ICE2_PHONE3: $("#ICE2_PHONE3").val(),
                    ICE2_REL: $("#ICE2_REL").val()
                });
            }
        }}
    });
    $( "#ens_form").accordion({
        active:0,
        header:'div.header',
        fillSpace:false,
        clearStyle:true
    });
    initializeHandlers();
    initialvalidation();
}
