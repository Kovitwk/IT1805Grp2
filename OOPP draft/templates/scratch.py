if form.cleaned_data['dataset_image']:
   # dataset.dataset_image = form.cleaned_data['dataset_image']
    name = 'dataset%s.png' % (dataset.id)
    size = (200, 200)
    try:
        im = Image.open(form.cleaned_data['dataset_image'])
        im.save(name, 'PNG')
        print "saved file: ", im
    except IOError:
        # dont' save the image
        pass