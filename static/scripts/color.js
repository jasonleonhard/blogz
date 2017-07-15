function updateR(R) {
    document.querySelector('#R_number').value = R;
    document.querySelector('#R_range').value = R;
}
function updateG(G) {
    document.querySelector('#G_number').value = G;
    document.querySelector('#G_range').value = G;
}
function updateB(B) {
    document.querySelector('#B_number').value = B;
    document.querySelector('#B_range').value = B;
}
function updateA(A) {
    document.querySelector('#A_number').value = A;
    document.querySelector('#A_range').value = A;
}

function changeColor() {
    var R = document.querySelector('#R_number').value;
    var G = document.querySelector('#G_number').value;
    var B = document.querySelector('#B_number').value;
    var A = document.querySelector('#A_number').value;

    var current_color = "rgba(" + R + ", " + G + ", " + B +  ", " + A + ")";
    var current_color_modal = "rgba(" + R + ", " + G + ", " + B +  ", 1 )";

    console.log(current_color);

    $('body').css('background', current_color)
    $('.modal-content').css('background', current_color_modal)

    document.getElementById("rgba_btn").innerHTML = current_color;
    // document.getElementById("rgba2").innerHTML = current_color;
    // document.getElementById("rgba2").color = current_color;

    // if (R == 0 && G == 255 && B == 255 && A == 1) {
    //     var color_name = document.querySelector('#color_name');
    //     color_name.innerHTML = 'aqua';
    //     document.getElementById("rgba").innerHTML = current_color;
    // } else {
    //     // color_name.innerHTML = current_color;
    //     // $("#rgb").text(current_color);
    //     // document.getElementById("rgba").innerHTML = '';
    //     document.getElementById("rgba").innerHTML = '';
    // }
}

function logBackgroundColor(_this) {
    // body background, not color of element
    console.log(_this.innerHTML);
}

function logColor(_this) {
    // element text color
    console.log($('#rgba_btn').css('color'))
}

function toggleColor(_this) {
    // target one element by id
    // var cur = $('#rgba_btn').css('color')

    // target currently clicked element
    // var cur = $(_this).css('color')

    // target multiple elements maybe an array?
    // target all text!!!
    // var cur = $('body').css('color')
    var cur = $('panel').css('color')

    if (cur == 'rgb(255, 255, 255)'){
        $(_this).css('color', 'black')
    }
    if (cur == 'rgb(0, 0, 0)') {
        $(_this).css('color', 'white')
    }
}

// works for all except the tick marks...
function toggleColors(_this) {
    // target currently clicked element
    var cur = $(_this).css('color')

    // if white
    if (cur == 'rgb(255, 255, 255)'){
        // $('*').css('color', 'black')
        // $('option').css('color', 'black')
        $('input#R_number').css('color', 'black')
        $('input#G_number').css('color', 'black')
        $('input#B_number').css('color', 'black')
        $('input#A_number').css('color', 'black')
        // $('#R').css('color', 'black') // label changes
        // $('#G').css('color', 'black') // label changes
        // $('#B').css('color', 'black') // label changes
        // $('#A').css('color', 'black') // label changes
        // $(_this).css('color', 'black')
        $('#title').css('color', 'black')
        $('#R_label').css('color', 'black')
        $('#G_label').css('color', 'black')
        $('#B_label').css('color', 'black')
        $('#A_label').css('color', 'black')
        $('#rgba_pos').css('color', 'black')
        $('#rgba_btn').css('color', 'black')
        $('#position').css('color', 'black')
        $('#color_name').css('color', 'black')
        $('#technicolor_btn').css('color', 'black')
        $('#myBtn').css('color', 'black')
        $('.modal-content').css('color', 'black')
    }
    // black
    if (cur == 'rgb(0, 0, 0)') {
        // $('*').css('color', 'white')
        // $('option').css('color', 'white')
        $('input#R_number').css('color', 'black')
        $('input#G_number').css('color', 'black')
        $('input#B_number').css('color', 'black')
        $('input#A_number').css('color', 'black')
        // $('#R').css('color', 'white') // label changes
        // $('#G').css('color', 'white') // label changes
        // $('#B').css('color', 'white') // label changes
        // $('#A').css('color', 'white') // label changes
        // $(_this).css('color', 'white')
        $('#title').css('color', 'white')
        $('#R_label').css('color', 'white')
        $('#G_label').css('color', 'white')
        $('#B_label').css('color', 'white')
        $('#A_label').css('color', 'white')
        $('#rgba_pos').css('color', 'white')
        $('#rgba_btn').css('color', 'white')
        $('#position').css('color', 'white')
        $('#color_name').css('color', 'white')
        $('#technicolor_btn').css('color', 'white')
        $('#myBtn').css('color', 'white')
        $('.modal-content').css('color', 'white')
    }
}

// WIP: similar to toggleColor
    // listens to the body background and
    // changes this color dark when A value is low like 0 to 0.8
    // and light when A value is 0.81 to 1.0
