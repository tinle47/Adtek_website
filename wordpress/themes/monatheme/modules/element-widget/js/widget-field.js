jQuery(document).ready(function($) {

    $(document).on("click", ".upload_image_button", function(e) {
        e.preventDefault(e);
        var $button = $(this);

        var file_frame = wp.media.frames.file_frame = wp.media({
            title: 'Select or upload image',
            library: {
                type: 'image'
            },
            button: {
                text: 'Select'
            },
            multiple: false
        });

        file_frame.on('select', function() {

            var attachment = file_frame.state().get('selection').first().toJSON();

            $button.closest('.box-field-image').find('input').attr('value', attachment.url);
            $button.closest('.box-field-image').find('.w-image-review').attr('src', attachment.url);

        });

        file_frame.open();
        $('input[name="savewidget"]').prop('disabled', false);
    });

    $(document).on("click", ".remove_image_button", function(e) {
        e.preventDefault();
        var $button = $(this);
        $button.closest('.box-field-image').find('input').attr('value', '');
        $button.closest('.box-field-image').find('.w-image-review').attr('src', '');
        $('input[name="savewidget"]').prop('disabled', false);
    });

    //repeater
    $(document).on("click", ".add_row_button", function(e) {
        e.preventDefault(e);
        var $this = $(this),
            $repeater = $this.closest('.repeaters').find('[data-repeatable]'),
            count = ($repeater.length - 1),
            $clone = $repeater.first().clone();

        $clone.find('input').each(function() {
            var $this = $(this);
            $this.attr('id', $this.attr('id').replace('rowCloneindex', 'row-' + count + ''));
            $this.attr('name', $this.attr('name').replace('rowCloneindex', 'row-' + count + ''));
            $this.attr('disabled', false);

        });

        $clone.find('input:not(:checkbox):not(:radio)').each(function() {
            var $this = $(this);
            $this.attr('value', '');
        });

        $clone.find('textarea').each(function() {
            var $this = $(this);
            $this.attr('id', $this.attr('id').replace('rowCloneindex', 'row-' + count + ''));
            $this.attr('name', $this.attr('name').replace('rowCloneindex', 'row-' + count + ''));
            $this.attr('disabled', false);
            $this.text('');
        });

        $clone.find('img').each(function() {
            var $this = $(this);
            $this.attr('src', '');
        });

        $clone.find('select').each(function() {
            var $this = $(this);
            $this.attr('id', $this.attr('id').replace('rowCloneindex', 'row-' + count + ''));
            $this.attr('name', $this.attr('name').replace('rowCloneindex', 'row-' + count + ''));
            $this.find('option:not(:disabled)').attr('selected', false);
            $this.attr('disabled', false);
        });

        $clone.find('input[type="radio"]').each(function() {
            var $this = $(this);
            $this.attr('checked', false);
        });

        $clone.find('input[type="checkbox"]').each(function() {
            var $this = $(this);
            $this.attr('checked', false);
        });

        $clone.find('label').each(function() {
            var $this = $(this);
            $this.attr('for', $this.attr('for').replace('rowCloneindex', 'row-' + count + ''));
        });

        $clone.find('#get_result_gallery').each(function() {
            var $this = $(this);
            $this.attr('data-gallery_id', $this.attr('data-gallery_id').replace('rowCloneindex', 'row-' + count + ''));
            $this.attr('data-gallery_name', $this.attr('data-gallery_name').replace('rowCloneindex', 'row-' + count + ''));
        });

        $clone.find('.render-gallery-images').each(function() {
            var $this = $(this);
            $this.html('');
        });

        $clone.find('.box-row-head span').each(function() {
            var $this = $(this);
            $this.text(count + 1);
        });

        $clone.attr('data-row_id', count);

        $clone.removeClass('rowCloneindex');

        $clone.insertBefore($this);

        $clone.find('.box-field-gallery').each(function() {
            var $this = $(this);
            WidgetMakeUlSortGallery();
        });

        WidgetMakeUlSortable();

        $('input[name="savewidget"]').prop('disabled', false);
    });

    // row remove
    $(document).on("click", ".remove_row_button", function(e) {
        e.preventDefault(e);
        if (confirm('Bạn muốn xóa dòng này ?')) {
            var $this = $(this),
                $repeater = $this.closest('.repeaters').find('[data-repeatable]'),
                count = $repeater.length;

            $this.closest('.field-row-repeater').remove();
            $('input[name="savewidget"]').prop('disabled', false);
        } else {
            return false;
        }
    });

    // gallery
    $(document).on("click", ".upload_gallery_button", function(e) {
        e.preventDefault(e);
        var $button = $(this),
            $gallerys = $button.closest('.box-field-gallery').find('.gallery-column'),
            count = $gallerys.length;

        var input_name = $button.closest('.box-field-gallery').find('#get_result_gallery').attr('data-gallery_name');
        var input_id = $button.closest('.box-field-gallery').find('#get_result_gallery').attr('data-gallery_id');
        var input_class = $button.closest('.box-field-gallery').find('#get_result_gallery').attr('data-gallery_class');
        var image_width = $button.closest('.box-field-gallery').find('#get_result_gallery').attr('data-gallery_width');

        var file_gallery_frame = wp.media.frames.file_frame = wp.media({
            title: 'Select or upload image',
            library: {
                type: 'image'
            },
            button: {
                text: 'Select'
            },
            multiple: true
        });

        file_gallery_frame.on('select', function() {

            var attachments = file_gallery_frame.state().get('selection').map(

                function(attachment) {

                    attachment.toJSON();
                    return attachment;

                });

            var i;

            for (i = 0; i < attachments.length; ++i) {

                var image_url = attachments[i].attributes.url;

                var galleryitems = '<div data-id="' + (i + count) + '" class="gallery-column"><div class="preview-image-item"><img style="width:' + image_width + 'px;max-width: ' + image_width + 'px;height:auto" class="' + input_class + '" id="' + input_id + '-' + (i + count) + '" src="' + image_url + '" /><input type="hidden" id="' + input_id + '" name="' + input_name + '[' + (i + count) + ']" value="' + image_url + '" /><div class="preview-image-action"><a href="javascript:;" class="act-remove-image">Xóa</a></div></div></div>';
                $button.closest('.box-field-gallery').find('.render-gallery-images').append(galleryitems);

            }
        });

        file_gallery_frame.open();
        $('input[name="savewidget"]').prop('disabled', false);

    });

    // gallery remove
    $(document).on("click", ".act-remove-image", function(e) {
        e.preventDefault(e);
        var $button = $(this);
        $action = $button.closest('.box-field-gallery .gallery-column').remove();
        $('input[name="savewidget"]').prop('disabled', false);
    });

    // show/hide row
    $(document).on("click", ".box-row-head", function(e) {
        e.preventDefault(e);
        var $box = $(this);
        if ($box.closest('.field-row-repeater').find('.box-row-repeaters').hasClass('hide')) {
            $box.closest('.field-row-repeater').find('.box-row-repeaters').removeClass('hide');
            $box.closest('.field-row-repeater').find('.box-row-repeaters').show();
        } else {
            $box.closest('.field-row-repeater').find('.box-row-repeaters').addClass('hide');
            $box.closest('.field-row-repeater').find('.box-row-repeaters').hide();
        }
    });

});