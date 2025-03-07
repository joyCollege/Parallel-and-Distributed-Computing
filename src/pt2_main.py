def lab4_2():
    from time import time
    from .pt2_read_images import read_path
    from .calc_print_analysis import calc_print_analysis
    from .pt2_save_and_load import save_processed_images, load_processed_images
    from .pt2_feature_extraction import feature_extraction
    from .pt2_model_development import model_development

    nonparallel_time = time()
    yes_images, no_images = read_path()
    # yes_images, no_images = yes_images[0:6], no_images[0:6] #comment out if you want a full run
    nonparallel_time = nonparallel_time - time()

    from .pt2_process_image_sequential import sequential_run
    sequential_time, yes_processed_sequential, no_processed_sequential = sequential_run(yes_images, no_images)
    save_processed_images(yes_processed_sequential, "yes_full_processed_images.pkl")
    save_processed_images(no_processed_sequential, "no_full_processed_images.pkl")
    print()

    from .pt2_process_image_pooling import pooling_run
    pooling_time, yes_processed_pooling, no_processed_pooling = pooling_run(yes_images, no_images)
    calc_print_analysis(sequential_time, pooling_time, pooling_time/(pooling_time+nonparallel_time), "pooling process_image")

    # sequential_time = 9717.20770573616
    # pooling_time = 1908.0378203392029
    # calc_print_analysis(sequential_time, pooling_time, pooling_time/(pooling_time+nonparallel_time), "pooling process_image")

    from .pt2_process_image_hessian import hessian_run
    hessian_time, yes_processed_hessian, no_processed_hessian = hessian_run(yes_images, no_images)
    calc_print_analysis(sequential_time, hessian_time, hessian_time/(hessian_time+nonparallel_time), "first main hessian_run process_image")
    
    from .pt2_process_image_threadPool import thread_run
    thread_time, yes_processed_thread, no_processed_thread = thread_run(yes_images, no_images)
    calc_print_analysis(sequential_time, thread_time, thread_time/(thread_time+nonparallel_time), "thread_run process_image")

    from .pt2_process_image_split import split_run
    split_time, yes_processed_split, no_processed_split = split_run(yes_images, no_images)
    calc_print_analysis(sequential_time, split_time, split_time/(split_time+nonparallel_time), "split_run process_image")
    
    from .pt2_process_images_hybrid import hybrid_run
    hybrid_time, yes_processed_hybrid, no_processed_hybrid = hybrid_run(yes_images, no_images)
    calc_print_analysis(sequential_time, hybrid_time, hybrid_time/(hybrid_time+nonparallel_time), "hybrid_run process_image")
    
    # yes_processed_sequential = load_processed_images("yes_full_processed_images.pkl")
    # no_processed_sequential = load_processed_images("no_full_processed_images.pkl")
    # shuffled_dataset = feature_extraction(yes_processed_sequential, no_processed_sequential)
    # model_development(shuffled_dataset)
    
    #python3 main.py | tee output.txt