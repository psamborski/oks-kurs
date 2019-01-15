$(function(){
    $('.modal').modal();

    $('.chosen-course-date').text($('.course-radio:checked + .course-card .course-date').text());
    $('input[type=radio][name=courseId]').change(function() {
        $('.chosen-course-date').text($('.course-radio:checked + .course-card .course-date').text());
    });
});
