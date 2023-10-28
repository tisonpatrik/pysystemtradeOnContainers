def process_table(map_item):
    full_path = file_path_validator.get_full_path(
        map_item.directory, map_item.file_name
    )

    raw_data = csv_files_service.load_csv(full_path)

    renamed = tables_helper.rename_columns(raw_data, map_item.columns_mapping)

    return renamed
