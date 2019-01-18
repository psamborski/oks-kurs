$(function(){
    $('.modal').modal();

    $('.chosen-course-date').text($('.radio-course:checked + .col .card-panel .course-card .course-date-hour .course-date').text());
    $('input[type=radio][name=courseId]').change(function() {
        $('.chosen-course-date').text($('.radio-course:checked + .col .card-panel .course-card .course-date-hour .course-date').text());
    });
});
