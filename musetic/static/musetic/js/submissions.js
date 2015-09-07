/**
 * submissions.js v1.0.0
 */

(function() {
    $.submissions = function() {


        /**
         * Variables
         */
        var submissionsOverlay = $('.submissions-overlay'),

            // Icons
            categoryIcon = $('.submissions-category'),
            categoryText = $('.category-text'),
            userIcon = $('.submissions-user'),
            userText = $('.user-text'),
            flagIcon = $('.submissions-flag'),
            flagIconDisabled = $('.submissions-flag:disabled'),
            moreIcon = $('.submissions-more'),

            // VoteForm
            voteForm = $('.vote-form'),

            // FlagForm
            flagForm = $('.flag-form'),
            flagCancel = $('button.flag-cancel'),
            flagSubmit = $('.flag-form input[name="submit"]'),

            // Upvote Buttons
            voteButtonDisabled = $('.upvote-button.vote-disabled'),
            voteButtonUnvoted = $('.upvote-button.unvoted'),
            voteButtonVoted = $('.upvote-button.voted'),
            numVotesDisabled = $('.num-votes.vote-disabled'),
            numVotesUnvoted = $('.num-votes.unvoted'),
            numVotesVoted = $('.num-votes.voted'),

            // Delay
            t = 200;

        /**
         * Voting AJAX Call
         */
        voteForm.submit(function (e) {
            e.preventDefault();
            var btn = $("button", this);
            btn.attr('disabled', true);
            $.post("/vote/", $(this).serializeArray(),
                function (data) {
                    if (data["voteobj"]) {
                        btn.removeClass('unvoted');
                        btn.addClass('voted');
                    }
                });
            btn.attr('disabled', false);
        });

        /**
         * Flagging Form
         */
        flagIcon.click(function() {
            $(this).closest('div').find(flagForm).fadeIn(t);
            $(this).closest('div').find(flagCancel).fadeIn(t);
            $(this).closest('div').find('textarea').focus();
        });
        flagCancel.click(function() {
            $(this).closest('div').find(flagForm).fadeOut(t);
            $(this).fadeOut(t);
        });
        flagForm.submit(function(e) {
            e.preventDefault();
            $.ajax({
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                data: $(this).serialize(),
                dataType: 'json',
                success: function () {
                    flagForm.fadeOut(t);
                },
                error: function () {
                    alert('The form failed to submit, you probably lost a connection');
                }
            }).done(function (data) {
                if (console && console.log) {
                    console.log("Sample of data", data);
                }
            });
        });


        /**
         * Submissions Hover Effects
         */
        voteButtonUnvoted.click(function() {
            $(this).animate({
                opacity: 0
            }, t);
            $(this).next(numVotesUnvoted).animate({
                opacity: 1,
                bottom: 15
            }, t);
        });
    }
})(jQuery);

/**
 * Load all javascript for submissions
 */
$(document).ready(function() {
    $.submissions();
});


/**
 * Submissions Loading Effects
 */
$(document).ready(function () {
    $('.submissions-loading-overlay').fadeOut();
});