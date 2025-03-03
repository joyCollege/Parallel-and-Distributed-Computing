def lab4_2():
    from time import time
    from .pt2_read_images import read_path
    from .calc_print_analysis import calc_print_analysis
    from .pt2_save_and_load import save_processed_images, load_processed_images

    nonparallel_time = time()
    yes_images, no_images = read_path()
    # yes_images, no_images = yes_images[0:2], no_images[0:2] #comment out if you want a full run
    nonparallel_time = nonparallel_time - time()

    from .pt2_process_image_sequential import sequential_run
    sequential_time, yes_processed_sequential, no_processed_sequential = sequential_run(yes_images, no_images)
    save_processed_images(yes_processed_sequential, "yes_full_processed_images.pkl")
    save_processed_images(no_processed_sequential, "no_full_processed_images.pkl")

    from .pt2_process_image_pooling import pooling_run
    pooling_time, yes_processed_pooling, no_processed_pooling = pooling_run(yes_images, no_images)
    calc_print_analysis(sequential_time, pooling_time, pooling_time/(pooling_time+nonparallel_time), "pooling process_image")

    from .pt2_process_image_hessian import hessian_run
    hessian_time, yes_processed_hessian, no_processed_hessian = hessian_run(yes_images, no_images)
    calc_print_analysis(sequential_time, hessian_time, hessian_time/(hessian_time+nonparallel_time), "hessian process_image (combined threading + pooling)")


