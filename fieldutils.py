def get_field_display_order(field):
    education_dict = \
    {
        "Tidak/Belum Sekolah": 1, "Tidak/Belum Tamat SD": 2, "SD": 3, 
        "SMP": 4, "SMA": 5, "D1/D2": 6, "D3": 7, "S1/D4": 8, "S2": 9, 
        "S3": 10
    }
    occupation_dict = \
    {
        "Akuntan": 0,
        "Anggota BPK": 1,
        "Anggota DPD": 2,
        "Anggota DPR-RI": 3,
        "Anggota DPRD Kabupaten/Kota": 4,
        "Anggota DPRD Provinsi": 5,
        "Anggota Kabinet/Kementerian": 6,
        "Anggota Mahkamah Konstitusi": 7,
        "Apoteker": 8,
        "Arsitek": 9,
        "Belum/Tidak Bekerja": 10,
        "Biarawati": 11,
        "Bidan": 12,
        "Bupati": 13,
        "Buruh Harian Lepas": 14,
        "Buruh Nelayan/Perikanan": 15,
        "Buruh Peternakan": 16,
        "Buruh Tani/Perkebunan": 17,
        "Dokter": 18,
        "Dosen": 19,
        "Duta Besar": 20,
        "Gubernur": 21,
        "Guru": 22,
        "Imam Mesjid": 23,
        "Industri": 24,
        "Juru Masak": 25,
        "Karyawan BUMD": 26,
        "Karyawan BUMN": 27,
        "Karyawan Honorer": 28,
        "Karyawan Swasta": 29,
        "Kepala Desa": 30,
        "Kepolisian RI": 31,
        "Konstruksi": 32,
        "Konsultan": 33,
        "Lainnya": 34,
        "Mekanik": 35,
        "Mengurus Rumah Tangga": 36,
        "Nelayan/Perikanan": 37,
        "Notaris": 38,
        "Paraji": 39,
        "Paranormal": 40,
        "Pastor": 41,
        "Pedagang": 42,
        "Pegawai Negeri Sipil": 43,
        "Pelajar/Mahasiswa": 44,
        "Pelaut": 45,
        "Pembantu Rumah Tangga": 46,
        "Penata Busana": 47,
        "Penata Rambut": 48,
        "Penata Rias": 49,
        "Pendeta": 50,
        "Peneliti": 51,
        "Pengacara": 52,
        "Pensiunan": 53,
        "Penterjemah": 54,
        "Penyiar Radio": 55,
        "Penyiar Televisi": 56,
        "Perancang Busana": 57,
        "Perangkat Desa": 58,
        "Perawat": 59,
        "Perdagangan": 60,
        "Petani/Pekebun/Peternak": 61,
        "Pialang": 62,
        "Pilot": 63,
        "Promotor Acara": 64,
        "Psikiater/Psikolog": 65,
        "Seniman": 66,
        "Sopir": 67,
        "Tabib": 68,
        "Tentara Nasional Indonesia": 69,
        "Transportasi": 70,
        "Tukang Batu": 71,
        "Tukang Cukur": 72,
        "Tukang Gigi": 73,
        "Tukang Jahit": 74,
        "Tukang Kayu": 75,
        "Tukang Las/Pandai Besi": 76,
        "Tukang Listrik": 77,
        "Tukang Sol Sepatu": 78,
        "Ustadz/Mubaligh": 79,
        "Wakil Gubernur": 80,
        "Wakil Presiden": 81,
        "Walikota": 82,
        "Wartawan": 83,
        "Wiraswasta": 84  
    }
    marriage_dict = \
    {
        'Belum Kawin': 0,
        'Kawin': 1,
        'Cerai Hidup': 2,
        'Cerai Mati': 3
    }
    religion_dict = \
    {
        'Islam': 0,
        'Kristen': 1,
        'Katholik': 2,
        'Hindu': 3,
        'Budha': 4,
        'Khonghuchu': 5,
        'Aliran Kepercayaan': 6
    }
    demographics_dict = \
    {
        'Luas Wilayah'   : 0,
        'Kepadatan'      : 1,
        '35-39 Laki-Laki': 2,
        '35-39 Perempuan': 3,
        '40-44 Laki-Laki': 4,
        '40-44 Perempuan': 5,
        '45-49 Laki-Laki': 6,
        '45-49 Perempuan': 7,
        '50-54 Laki-Laki': 8,
        '50-54 Perempuan': 9,
        '55-59 Laki-Laki': 10,
        '55-59 Perempuan': 11,
        '60-64 Laki-Laki': 12,
        '60-64 Perempuan': 13,
        '65-69 Laki-Laki': 14,
        '65-69 Perempuan': 15,
        '70-74 Laki-Laki': 16,
        '70-74 Perempuan': 17,
        '>75 Laki-Laki'  : 18,
        '>75  Perempuan' : 19
    }

    if field in list(education_dict.keys()):
        return education_dict[field]
    elif field in list(occupation_dict.keys()):
        return occupation_dict[field]
    elif field in list(marriage_dict.keys()):
        return marriage_dict[field]
    elif field in list(religion_dict.keys()):
        return religion_dict[field]
    elif field in list(demographics_dict.keys()):
        return demographics_dict[field]

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