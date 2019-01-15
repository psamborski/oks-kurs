$(function(){
    $('.modal').modal();

    $('.chosen-course-date').text($('.course-radio:checked + .course-banner .course-date').text());
    $('input[type=radio][name=courseId]').change(function() {
        $('.chosen-course-date').text($('.course-radio:checked + .course-banner .course-date').text());
    });
});
