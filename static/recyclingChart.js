$(document).ready(function() {
    // Delete user
    $('.btn-danger').click(function(e) {
        e.preventDefault();
        let userId = $(this).attr('href').split('/')[2];
        if (confirm('Are you sure you want to delete this user?')) {
            $.ajax({
                url: '/delete-user/' + userId,
                type: 'DELETE',
                success: function(result) {
                    location.reload();
                }
            });
        }
    });

    // Delete collection
    $('.btn-danger').click(function(e) {
        e.preventDefault();
        let collectionId = $(this).attr('href').split('/')[2];
        if (confirm('Are you sure you want to delete this collection?')) {
            $.ajax({
                url: '/delete-collection/' + collectionId,
                type: 'DELETE',
                success: function(result) {
                    location.reload();
                }
            });
        }
    });

    // Delete recycling
    $('.btn-danger').click(function(e) {
        e.preventDefault();
        let recyclingId = $(this).attr('href').split('/')[2];
        if (confirm('Are you sure you want to delete this recycling record?')) {
            $.ajax({
                url: '/delete-recycling/' + recyclingId,
                type: 'DELETE',
                success: function(result) {
                    location.reload();
                }
            });
        }
    });
});