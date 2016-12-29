def get_field_stage(category, field):
    education_list = \
    {
        "Tidak/Belum Sekolah": 1, "Tidak/Belum Tamat SD": 2, "SD": 3, 
        "SMP": 4, "SMA": 5, "D1/D2": 6, "D3": 7, "S1/D4": 8, "S2": 9, 
        "S3": 10
    }

    if category == "education":
        return education_list[field]

def get_field_list(collection):
    """
    Get list of all non-spacetime fields in a standard 
    collection document
    """
    # list all space/time/id fields in document
    spacetimeid_list = ['Kecamatan', 'Kabupaten', 'Kelurahan', 
                        'Tahun', "_id"]
    # list all education level fields
    return [field for field in list(collection.find_one().keys()) 
            if field not in spacetimeid_list]