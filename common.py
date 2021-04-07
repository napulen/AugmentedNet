import os

RANDOMSEED = 1337

# Number of decimals to the right of the decimal point
FLOATSCALE = 4

# Sixteenth notes
FRAMEBASENOTE = 16
FIXEDOFFSET = round(4.0 / FRAMEBASENOTE, FLOATSCALE)

SEQUENCELENGTH = 64

BATCHSIZE = 32

DATASETDIR = "dataset"
DATASETSUMMARYFILE = os.path.join(DATASETDIR, "dataset_summary.tsv")

ANNOTATIONSCOREDUPLES = {
    "bps-01-op002-no1-1": (
        "When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op002_No1/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_01_01.mxl",
    ),
    "bps-02-op002-no2-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op002_No2/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_02_01.mxl",
    ),
    "bps-03-op002-no3-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op002_No3/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_03_01.mxl",
    ),
    "bps-04-op007-1": (
        "When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op007/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_04_01.mxl",
    ),
    "bps-05-op010-no1-1": (
        "When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op010_No1/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_05_01.mxl",
    ),
    "bps-06-op010-no2-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op010_No2/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_06_01.mxl",
    ),
    "bps-07-op010-no3-1": (
        "When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op010_No3/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_07_01.mxl",
    ),
    "bps-08-op013-pathetique-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op013(Pathetique)/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_08_01.mxl",
    ),
    "bps-09-op014-no1-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op014_No1/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_09_01.mxl",
    ),
    "bps-10-op014-no2-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op014_No2/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_10_01.mxl",
    ),
    "bps-11-op022-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op022/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_11_01.mxl",
    ),
    "bps-12-op026-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op026/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_12_01.mxl",
    ),
    "bps-13-op027-no1-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op027_No1/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_13_01.mxl",
    ),
    "bps-14-op027-no2-moonlight-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op027_No2(Moonlight)/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_14_01.mxl",
    ),
    "bps-15-op028-pastorale-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op028(Pastorale)/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_15_01.mxl",
    ),
    "bps-16-op031-no1-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op031_No1/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_16_01.mxl",
    ),
    "bps-17-op031-no2-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op031_No2/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_17_01.mxl",
    ),
    "bps-18-op031-no3-1": (
        "When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op031_No3/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_18_01.mxl",
    ),
    "bps-19-op049-no1-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op049_No1/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_19_01.mxl",
    ),
    "bps-20-op049-no2-1": (
        "When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op049_No2/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_20_01.mxl",
    ),
    "bps-21-op053-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op053/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_21_01.mxl",
    ),
    "bps-22-op054-1": (
        "When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op054/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_22_01.mxl",
    ),
    "bps-23-op057-appassionata-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op057(Appassionata)/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_23_01.mxl",
    ),
    "bps-24-op078-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op078/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_24_01.mxl",
    ),
    "bps-25-op079-sonatina-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op079(Sonatina)/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_25_01.mxl",
    ),
    "bps-26-op081a-les-adieux-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op081a(Les_Adieux)/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_26_01.mxl",
    ),
    "bps-27-op090-1": (
        "When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op090/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_27_01.mxl",
    ),
    "bps-28-op101-1": (
        "When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op101/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_28_01.mxl",
    ),
    "bps-29-op106-hammerklavier-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op106(Hammerklavier)/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_29_01.mxl",
    ),
    "bps-30-op109-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op109/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_30_01.mxl",
    ),
    "bps-31-op110-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op110/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_31_01.mxl",
    ),
    "bps-32-op111-1": (
        "AlignedWiR/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op111/1/analysis.txt",
        "functional-harmony-micchi/data/BPS/scores/bps_32_01.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-1-4-mayenlied": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/4_Mayenlied/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/4_Mayenlied/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-1-1-schwanenlied": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/1_Schwanenlied/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/1_Schwanenlied/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-1-6-gondellied": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/6_Gondellied/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/6_Gondellied/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-1-5-morgenstandchen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/5_Morgenständchen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/5_Morgenständchen/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-1-3-warum-sind-denn-die-rosen-so-blass": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/3_Warum_sind_denn_die_Rosen_so_blass/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/3_Warum_sind_denn_die_Rosen_so_blass/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-3-lieder-1-sehnsucht": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/3_Lieder/1_Sehnsucht/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/3_Lieder/1_Sehnsucht/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-9-2-ferne": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/2_Ferne/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/2_Ferne/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-9-4-die-fruhen-graber": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/4_Die_frühen_Gräber/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/4_Die_frühen_Gräber/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-9-1-die-ersehnte": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/1_Die_Ersehnte/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/1_Die_Ersehnte/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-9-3-der-rosenkranz": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/3_Der_Rosenkranz/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/3_Der_Rosenkranz/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-6-lieder-op-9-5-der-maiabend": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/5_Der_Maiabend/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/5_Der_Maiabend/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-5-lieder-op-10-4-im-herbste": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/4_Im_Herbste/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/4_Im_Herbste/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-5-lieder-op-10-3-abendbild": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/3_Abendbild/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/3_Abendbild/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-5-lieder-op-10-2-vorwurf": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/2_Vorwurf/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/2_Vorwurf/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-5-lieder-op-10-5-bergeslust": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/5_Bergeslust/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/5_Bergeslust/score.mxl",
    ),
    "wir-openscore-liedercorpus-hensel-5-lieder-op-10-1-nach-suden": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/1_Nach_Süden/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/1_Nach_Süden/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-6-lieder-op-13-6-die-stille-lotosblume": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/6_Die_stille_Lotosblume/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/6_Die_stille_Lotosblume/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-6-lieder-op-13-1-ich-stand-in-dunklen-traumen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/1_Ich_stand_in_dunklen_Träumen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/1_Ich_stand_in_dunklen_Träumen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-6-lieder-op-13-3-liebeszauber": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/3_Liebeszauber/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/3_Liebeszauber/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-6-lieder-op-13-2-sie-liebten-sich-beide": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/2_Sie_liebten_sich_beide/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/6_Lieder,_Op.13/2_Sie_liebten_sich_beide/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-lieder-op-12-04-liebst-du-um-schonheit": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/Lieder,_Op.12/04_Liebst_du_um_Schönheit/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/Lieder,_Op.12/04_Liebst_du_um_Schönheit/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-die-gute-nacht": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/_/Die_gute_Nacht/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Clara/_/Die_gute_Nacht/score.mxl",
    ),
    "wir-openscore-liedercorpus-coleridge-taylor-oh-the-summer": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Coleridge-Taylor,_Samuel/_/Oh,_the_Summer/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Coleridge-Taylor,_Samuel/_/Oh,_the_Summer/score.mxl",
    ),
    "wir-openscore-liedercorpus-franz-6-gesange-op-14-5-liebesfruhling": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Franz,_Robert/6_Gesänge,_Op.14/5_Liebesfrühling/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Franz,_Robert/6_Gesänge,_Op.14/5_Liebesfrühling/score.mxl",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-08-nachtzauber": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/08_Nachtzauber/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/08_Nachtzauber/score.mxl",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-19-die-nacht": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/19_Die_Nacht/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/19_Die_Nacht/score.mxl",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-13-der-scholar": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/13_Der_Scholar/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/13_Der_Scholar/score.mxl",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-14-der-verzweifelte-liebhaber": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/14_Der_verzweifelte_Liebhaber/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/14_Der_verzweifelte_Liebhaber/score.mxl",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-20-waldmadchen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/20_Waldmädchen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/20_Waldmädchen/score.mxl",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-04-das-standchen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/04_Das_Ständchen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/04_Das_Ständchen/score.mxl",
    ),
    "wir-openscore-liedercorpus-wolf-eichendorff-lieder-15-unfall": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/15_Unfall/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Wolf,_Hugo/Eichendorff-Lieder/15_Unfall/score.mxl",
    ),
    "wir-openscore-liedercorpus-chausson-7-melodies-op-2-7-le-colibri": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Chausson,_Ernest/7_Mélodies,_Op.2/7_Le_Colibri/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Chausson,_Ernest/7_Mélodies,_Op.2/7_Le_Colibri/score.mxl",
    ),
    "wir-openscore-liedercorpus-lang-6-lieder-op-25-4-lied-immer-sich-rein-kindlich-erfreun": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Lang,_Josephine/6_Lieder,_Op.25/4_Lied_(Immer_sich_rein_kindlich_erfreu’n)/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Lang,_Josephine/6_Lieder,_Op.25/4_Lied_(Immer_sich_rein_kindlich_erfreu’n)/score.mxl",
    ),
    "wir-openscore-liedercorpus-mahler-kindertotenlieder-4-oft-denk-ich-sie-sind-nur-ausgegangen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Mahler,_Gustav/Kindertotenlieder/4_Oft_denk’_ich,_sie_sind_nur_ausgegangen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Mahler,_Gustav/Kindertotenlieder/4_Oft_denk’_ich,_sie_sind_nur_ausgegangen/score.mxl",
    ),
    "wir-openscore-liedercorpus-mahler-kindertotenlieder-2-nun-seh-ich-wohl-warum-so-dunkle-flammen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Mahler,_Gustav/Kindertotenlieder/2_Nun_seh’_ich_wohl,_warum_so_dunkle_Flammen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Mahler,_Gustav/Kindertotenlieder/2_Nun_seh’_ich_wohl,_warum_so_dunkle_Flammen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-frauenliebe-und-leben-op-42-3-ich-kanns-nicht-fassen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Frauenliebe_und_Leben,_Op.42/3_Ich_kann’s_nicht_fassen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Frauenliebe_und_Leben,_Op.42/3_Ich_kann’s_nicht_fassen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-frauenliebe-und-leben-op-42-1-seit-ich-ihn-gesehen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Frauenliebe_und_Leben,_Op.42/1_Seit_ich_ihn_gesehen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Frauenliebe_und_Leben,_Op.42/1_Seit_ich_ihn_gesehen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-04-wenn-ich-in-deine-augen-seh": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/04_Wenn_ich_in_deine_Augen_seh’/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/04_Wenn_ich_in_deine_Augen_seh’/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-05-ich-will-meine-seele-tauchen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/05_Ich_will_meine_Seele_tauchen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/05_Ich_will_meine_Seele_tauchen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-16-die-alten-bosen-lieder": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/16_Die_alten,_bösen_Lieder/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/16_Die_alten,_bösen_Lieder/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-13-ich-hab-im-traum-geweinet": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/13_Ich_hab’_im_Traum_geweinet/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/13_Ich_hab’_im_Traum_geweinet/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-11-ein-jungling-liebt-ein-madchen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/11_Ein_Jüngling_liebt_ein_Mädchen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/11_Ein_Jüngling_liebt_ein_Mädchen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-07-ich-grolle-nicht": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/07_Ich_grolle_nicht/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/07_Ich_grolle_nicht/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-02-aus-meinen-tranen-spriessen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/02_Aus_meinen_Tränen_sprießen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/02_Aus_meinen_Tränen_sprießen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-09-das-ist-ein-floten-und-geigen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/09_Das_ist_ein_Flöten_und_Geigen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/09_Das_ist_ein_Flöten_und_Geigen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-01-im-wunderschonen-monat-mai": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/01_Im_wunderschönen_Monat_Mai/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/01_Im_wunderschönen_Monat_Mai/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-10-hor-ich-das-liedchen-klingen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/10_Hör’_ich_das_Liedchen_klingen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/10_Hör’_ich_das_Liedchen_klingen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-03-die-rose-die-lilie": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/03_Die_Rose,_die_Lilie/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/03_Die_Rose,_die_Lilie/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-12-am-leuchtenden-sommermorgen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/12_Am_leuchtenden_Sommermorgen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/12_Am_leuchtenden_Sommermorgen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-06-im-rhein-im-heiligen-strome": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/06_Im_Rhein,_im_heiligen_Strome/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/06_Im_Rhein,_im_heiligen_Strome/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-08-und-wusstens-die-blumen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/08_Und_wüssten’s_die_Blumen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/08_Und_wüssten’s_die_Blumen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-15-aus-alten-marchen-winkt-es": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/15_Aus_alten_Märchen_winkt_es/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/15_Aus_alten_Märchen_winkt_es/score.mxl",
    ),
    "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-14-allnachtlich-im-traume": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/14_Allnächtlich_im_Traume/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schumann,_Robert/Dichterliebe,_Op.48/14_Allnächtlich_im_Traume/score.mxl",
    ),
    "wir-openscore-liedercorpus-jaell-4-melodies-1-a-toi": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Jaëll,_Marie/4_Mélodies/1_À_toi/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Jaëll,_Marie/4_Mélodies/1_À_toi/score.mxl",
    ),
    "wir-openscore-liedercorpus-chaminade-amoroso": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Chaminade,_Cécile/_/Amoroso/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Chaminade,_Cécile/_/Amoroso/score.mxl",
    ),
    "wir-openscore-liedercorpus-holmes-les-heures-4-lheure-dazur": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Holmès,_Augusta_Mary_Anne/Les_Heures/4_L’Heure_d’Azur/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Holmès,_Augusta_Mary_Anne/Les_Heures/4_L’Heure_d’Azur/score.mxl",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-04-wachtelwacht": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/04_Wachtelwacht/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/04_Wachtelwacht/score.mxl",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-03-die-blume-der-blumen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/03_Die_Blume_der_Blumen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/03_Die_Blume_der_Blumen/score.mxl",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-02-der-traurige-wanderer": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/02_Der_traurige_Wanderer/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/02_Der_traurige_Wanderer/score.mxl",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-05-betteley-der-vogel": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/05_Betteley_der_Vögel/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/05_Betteley_der_Vögel/score.mxl",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-09-hier-liegt-ein-spielmann-begraben": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/09_Hier_liegt_ein_Spielmann_begraben/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/09_Hier_liegt_ein_Spielmann_begraben/score.mxl",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-08-kaeuzlein": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/08_Kaeuzlein/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/08_Kaeuzlein/score.mxl",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-07-die-wiese": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/07_Die_Wiese/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/07_Die_Wiese/score.mxl",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-01-fruhlingsblumen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/01_Frühlingsblumen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Gesänge,_Op.3/01_Frühlingsblumen/score.mxl",
    ),
    "wir-openscore-liedercorpus-reichardt-zwolf-deutsche-und-italianische-romantische-gesange-10-ida-aus-ariels-offenbarungen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Deutsche_und_Italiänische_Romantische_Gesänge/10_Ida_(aus_Ariels_Offenbarungen)/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Zwölf_Deutsche_und_Italiänische_Romantische_Gesänge/10_Ida_(aus_Ariels_Offenbarungen)/score.mxl",
    ),
    "wir-openscore-liedercorpus-reichardt-sechs-lieder-von-novalis-op-4-5-noch-ein-bergmannslied": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Sechs_Lieder_von_Novalis,_Op.4/5_Noch_ein_Bergmannslied/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Reichardt,_Louise/Sechs_Lieder_von_Novalis,_Op.4/5_Noch_ein_Bergmannslied/score.mxl",
    ),
    "wir-openscore-liedercorpus-brahms-6-songs-op-3-3-liebe-und-fruhling-ii": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Brahms,_Johannes/6_Songs,_Op.3/3_Liebe_und_Frühling_II/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Brahms,_Johannes/6_Songs,_Op.3/3_Liebe_und_Frühling_II/score.mxl",
    ),
    "wir-openscore-liedercorpus-brahms-7-lieder-op-48-3-liebesklage-des-madchens": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Brahms,_Johannes/7_Lieder,_Op.48/3_Liebesklage_des_Mädchens/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Brahms,_Johannes/7_Lieder,_Op.48/3_Liebesklage_des_Mädchens/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-4-lieder-op-96-1-die-sterne-d-939": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/4_Lieder,_Op.96/1_Die_Sterne,_D.939/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/4_Lieder,_Op.96/1_Die_Sterne,_D.939/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-16-letzte-hoffnung": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/16_Letzte_Hoffnung/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/16_Letzte_Hoffnung/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-23-die-nebensonnen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/23_Die_Nebensonnen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/23_Die_Nebensonnen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-18-der-stuermische-morgen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/18_Der_stuermische_Morgen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/18_Der_stuermische_Morgen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-06-wasserfluth": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/06_Wasserfluth/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/06_Wasserfluth/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-09-irrlicht": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/09_Irrlicht/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/09_Irrlicht/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-04-erstarrung": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/04_Erstarrung/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/04_Erstarrung/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-14-der-greise-kopf": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/14_Der_greise_Kopf/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/14_Der_greise_Kopf/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-20-der-wegweiser": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/20_Der_Wegweiser/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/20_Der_Wegweiser/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-01-gute-nacht": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/01_Gute_Nacht/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/01_Gute_Nacht/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-12-einsamkeit-urspruengliche-fassung": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/12_Einsamkeit_(Urspruengliche_Fassung)/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/12_Einsamkeit_(Urspruengliche_Fassung)/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-13-die-post": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/13_Die_Post/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/13_Die_Post/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-03-gefrorne-thranen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/03_Gefror’ne_Thränen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/03_Gefror’ne_Thränen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-21-das-wirthshaus": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/21_Das_Wirthshaus/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/21_Das_Wirthshaus/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-17-im-dorfe": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/17_Im_Dorfe/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/17_Im_Dorfe/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-10-rast-spatere-fassung": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/10_Rast_(Spätere_Fassung)/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/10_Rast_(Spätere_Fassung)/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-05-der-lindenbaum": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/05_Der_Lindenbaum/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/05_Der_Lindenbaum/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-11-fruhlingstraum": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/11_Frühlingstraum/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/11_Frühlingstraum/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-02-die-wetterfahne": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/02_Die_Wetterfahne/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/02_Die_Wetterfahne/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-15-die-kraehe": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/15_Die_Kraehe/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/15_Die_Kraehe/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-24-der-leiermann-spatere-fassung": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/24_Der_Leiermann_(Spätere_Fassung)/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/24_Der_Leiermann_(Spätere_Fassung)/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-07-auf-dem-flusse": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/07_Auf_dem_Flusse/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/07_Auf_dem_Flusse/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-22-muth": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/22_Muth/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/22_Muth/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-08-ruckblick": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/08_Rückblick/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/08_Rückblick/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-19-tauschung": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/19_Täuschung/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Winterreise,_D.911/19_Täuschung/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-op-59-3-du-bist-die-ruh": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Op.59/3_Du_bist_die_Ruh/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Op.59/3_Du_bist_die_Ruh/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-die-schone-mullerin-d-795-12-pause": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Die_schöne_Müllerin,_D.795/12_Pause/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Die_schöne_Müllerin,_D.795/12_Pause/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-02-kriegers-ahnung": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/02_Kriegers_Ahnung/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/02_Kriegers_Ahnung/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-06-in-der-ferne": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/06_In_der_Ferne/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/06_In_der_Ferne/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-07-abschied": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/07_Abschied/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/07_Abschied/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-10-das-fischermadchen": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/10_Das_Fischermädchen/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/10_Das_Fischermädchen/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-11-die-stadt": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/11_Die_Stadt/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/11_Die_Stadt/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-05-aufenthalt": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/05_Aufenthalt/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/05_Aufenthalt/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-13-der-doppelganger": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/13_Der_Doppelgänger/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/13_Der_Doppelgänger/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-12-am-meer": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/12_Am_Meer/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/12_Am_Meer/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-14-die-taubenpost": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/14_Die_Taubenpost/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/14_Die_Taubenpost/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-09-ihr-bild": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/09_Ihr_Bild/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/09_Ihr_Bild/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-03-fruhlingssehnsucht": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/03_Frühlingssehnsucht/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/03_Frühlingssehnsucht/score.mxl",
    ),
    "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-08-der-atlas": (
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/08_Der_Atlas/analysis.txt",
        "When-in-Rome/Corpus/OpenScore-LiederCorpus/Schubert,_Franz/Schwanengesang,_D.957/08_Der_Atlas/score.mxl",
    ),
    "wir-bach-wtc-i-24": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/24/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/24/score.mxl",
    ),
    "wir-bach-wtc-i-15": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/15/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/15/score.mxl",
    ),
    "wir-bach-wtc-i-8": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/8/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/8/score.mxl",
    ),
    "wir-bach-wtc-i-3": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/3/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/3/score.mxl",
    ),
    "wir-bach-wtc-i-7": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/7/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/7/score.mxl",
    ),
    "wir-bach-wtc-i-17": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/17/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/17/score.mxl",
    ),
    "wir-bach-wtc-i-16": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/16/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/16/score.mxl",
    ),
    "wir-bach-wtc-i-11": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/11/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/11/score.mxl",
    ),
    "wir-bach-wtc-i-20": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/20/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/20/score.mxl",
    ),
    "wir-bach-wtc-i-19": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/19/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/19/score.mxl",
    ),
    "wir-bach-wtc-i-22": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/22/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/22/score.mxl",
    ),
    "wir-bach-wtc-i-9": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/9/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/9/score.mxl",
    ),
    "wir-bach-wtc-i-18": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/18/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/18/score.mxl",
    ),
    "wir-bach-wtc-i-1": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/1/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/1/score.mxl",
    ),
    "wir-bach-wtc-i-5": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/5/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/5/score.mxl",
    ),
    "wir-bach-wtc-i-4": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/4/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/4/score.mxl",
    ),
    "wir-bach-wtc-i-6": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/6/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/6/score.mxl",
    ),
    "wir-bach-wtc-i-10": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/10/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/10/score.mxl",
    ),
    "wir-bach-wtc-i-14": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/14/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/14/score.mxl",
    ),
    "wir-bach-wtc-i-23": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/23/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/23/score.mxl",
    ),
    "wir-bach-wtc-i-2": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/2/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/2/score.mxl",
    ),
    "wir-bach-wtc-i-21": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/21/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/21/score.mxl",
    ),
    "wir-bach-wtc-i-12": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/12/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/12/score.mxl",
    ),
    "wir-bach-wtc-i-13": (
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/13/analysis.txt",
        "When-in-Rome/Corpus/Etudes_and_Preludes/Bach,_Johann_Sebastian/The_Well-Tempered_Clavier_I/13/score.mxl",
    ),
    "wir-bach-chorales-1": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/1/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv269.mxl",
    ),
    "wir-bach-chorales-2": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/2/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv347.mxl",
    ),
    "wir-bach-chorales-3": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/3/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv153.1.mxl",
    ),
    "wir-bach-chorales-4": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/4/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv86.6.mxl",
    ),
    "wir-bach-chorales-5": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/5/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv267.mxl",
    ),
    "wir-bach-chorales-6": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/6/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv281.mxl",
    ),
    "wir-bach-chorales-7": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/7/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv17.7.mxl",
    ),
    "wir-bach-chorales-8": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/8/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv40.8.mxl",
    ),
    "wir-bach-chorales-9": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/9/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv248.12-2.mxl",
    ),
    "wir-bach-chorales-10": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/10/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv38.6.mxl",
    ),
    "wir-bach-chorales-12": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/12/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv65.2.mxl",
    ),
    "wir-bach-chorales-13": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/13/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv33.6.mxl",
    ),
    "wir-bach-chorales-14": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/14/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv184.5.mxl",
    ),
    "wir-bach-chorales-16": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/16/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv311.mxl",
    ),
    "wir-bach-chorales-17": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/17/analysis.txt",
        "AlignedBachChorales/bwv145.5.mxl",
    ),
    "wir-bach-chorales-18": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/18/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv318.mxl",
    ),
    "wir-bach-chorales-19": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/19/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv351.mxl",
    ),
    "wir-bach-chorales-20": (
        "When-in-Rome/Corpus/Early_Choral/Bach,_Johann_Sebastian/Chorales/20/analysis.txt",
        "music21_corpus/music21/corpus/bach/bwv302.mxl",
    ),
    "wir-monteverdi-madrigals-book-5-8": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/8/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/8/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-5-7": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/7/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/7/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-5-5": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/5/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/5/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-5-4": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/4/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_5/4/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-4-11": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/11/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/11/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-4-19": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/19/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/19/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-4-10": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/10/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/10/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-4-12": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/12/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/12/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-4-13": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/13/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_4/13/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-3-15": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/15/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/15/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-3-8": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/8/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/8/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-3-3": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/3/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/3/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-3-11": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/11/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/11/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-3-19": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/19/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/19/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-3-9": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/9/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/9/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-3-1": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/1/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/1/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-3-6": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/6/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/6/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-3-10": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/10/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/10/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-3-14": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/14/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/14/score.mxl",
    ),
    "wir-monteverdi-madrigals-book-3-13": (
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/13/analysis.txt",
        "When-in-Rome/Corpus/Early_Choral/Monteverdi,_Claudio/Madrigals_Book_3/13/score.mxl",
    ),
    "wir-variations-and-grounds-bach-b-minor-mass-bwv232-crucifixus": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Bach,_Johann_Sebastian/B_Minor_mass,_BWV232/Crucifixus/analysis.txt",
        "When-in-Rome/Corpus/Variations_and_Grounds/Bach,_Johann_Sebastian/B_Minor_mass,_BWV232/Crucifixus/score.mxl",
    ),
    "tavern-beethoven-op34-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/Op34/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/Opus34.mxl",
    ),
    "tavern-beethoven-op34-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/Op34/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/Opus34.mxl",
    ),
    "tavern-beethoven-op76-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/Op76/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/Opus76.mxl",
    ),
    "tavern-beethoven-op76-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/Op76/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/Opus76.mxl",
    ),
    "tavern-beethoven-woo-63-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_63/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B063.mxl",
    ),
    "tavern-beethoven-woo-63-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_63/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B063.mxl",
    ),
    "tavern-beethoven-woo-64-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_64/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B064.mxl",
    ),
    "tavern-beethoven-woo-64-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_64/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B064.mxl",
    ),
    "tavern-beethoven-woo-65-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_65/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B065.mxl",
    ),
    "tavern-beethoven-woo-65-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_65/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B065.mxl",
    ),
    "tavern-beethoven-woo-66-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_66/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B066.mxl",
    ),
    "tavern-beethoven-woo-66-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_66/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B066.mxl",
    ),
    "tavern-beethoven-woo-68-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_68/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B068.mxl",
    ),
    "tavern-beethoven-woo-68-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_68/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B068.mxl",
    ),
    "tavern-beethoven-woo-69-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_69/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B069.mxl",
    ),
    "tavern-beethoven-woo-69-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_69/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B069.mxl",
    ),
    "tavern-beethoven-woo-70-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_70/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B070.mxl",
    ),
    "tavern-beethoven-woo-70-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_70/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B070.mxl",
    ),
    "tavern-beethoven-woo-71-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_71/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B071.mxl",
    ),
    "tavern-beethoven-woo-71-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_71/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B071.mxl",
    ),
    "tavern-beethoven-woo-72-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_72/analysis_A.txt",
        "AlignedTavern/Beethoven/B072.mxl",
    ),
    "tavern-beethoven-woo-72-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_72/analysis_B.txt",
        "AlignedTavern/Beethoven/B072.mxl",
    ),
    "tavern-beethoven-woo-73-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_73/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B073.mxl",
    ),
    "tavern-beethoven-woo-73-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_73/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B073.mxl",
    ),
    "tavern-beethoven-woo-75-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_75/analysis_A.txt",
        "AlignedTavern/Beethoven/B075.mxl",
    ),
    "tavern-beethoven-woo-75-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_75/analysis_B.txt",
        "AlignedTavern/Beethoven/B075.mxl",
    ),
    "tavern-beethoven-woo-76-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_76/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B076.mxl",
    ),
    "tavern-beethoven-woo-76-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_76/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B076.mxl",
    ),
    "tavern-beethoven-woo-77-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_77/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B077.mxl",
    ),
    "tavern-beethoven-woo-77-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_77/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B077.mxl",
    ),
    "tavern-beethoven-woo-78-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_78/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B078.mxl",
    ),
    "tavern-beethoven-woo-78-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_78/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B078.mxl",
    ),
    "tavern-beethoven-woo-80-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_80/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B080.mxl",
    ),
    "tavern-beethoven-woo-80-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_80/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Beethoven/scores/B080.mxl",
    ),
    "tavern-mozart-k025-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K025/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K025.mxl",
    ),
    "tavern-mozart-k025-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K025/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K025.mxl",
    ),
    "tavern-mozart-k179-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K179/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K179.mxl",
    ),
    "tavern-mozart-k179-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K179/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K179.mxl",
    ),
    "tavern-mozart-k265-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K265/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K265.mxl",
    ),
    "tavern-mozart-k265-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K265/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K265.mxl",
    ),
    "tavern-mozart-k353-a": (
        "AlignedWiR/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K353/analysis_A.txt",
        "AlignedTavern/Mozart/K353.mxl",
    ),
    "tavern-mozart-k353-b": (
        "AlignedWiR/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K353/analysis_B.txt",
        "AlignedTavern/Mozart/K353.mxl",
    ),
    "tavern-mozart-k354-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K354/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K354.mxl",
    ),
    "tavern-mozart-k354-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K354/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K354.mxl",
    ),
    "tavern-mozart-k398-a": (
        "AlignedWiR/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K398/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K398.mxl",
    ),
    "tavern-mozart-k398-b": (
        "AlignedWiR/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K398/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K398.mxl",
    ),
    "tavern-mozart-k455-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K455/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K455.mxl",
    ),
    "tavern-mozart-k455-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K455/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K455.mxl",
    ),
    "tavern-mozart-k501-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K501/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K501.mxl",
    ),
    "tavern-mozart-k501-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K501/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K501.mxl",
    ),
    "tavern-mozart-k573-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K573/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K573.mxl",
    ),
    "tavern-mozart-k573-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K573/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K573.mxl",
    ),
    "tavern-mozart-k613-a": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K613/analysis_A.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K613.mxl",
    ),
    "tavern-mozart-k613-b": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K613/analysis_B.txt",
        "functional-harmony-micchi/data/Tavern/Mozart/scores/K613.mxl",
    ),
    "wir-variations-and-grounds-purcell-sonata-z807": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Purcell,_Henry/_/Sonata_Z807/analysis.txt",
        "When-in-Rome/Corpus/Variations_and_Grounds/Purcell,_Henry/_/Sonata_Z807/score.mxl",
    ),
    "wir-variations-and-grounds-purcell-chacony-z730": (
        "When-in-Rome/Corpus/Variations_and_Grounds/Purcell,_Henry/_/Chacony_Z730/analysis.txt",
        "When-in-Rome/Corpus/Variations_and_Grounds/Purcell,_Henry/_/Chacony_Z730/score.mxl",
    ),
    "abc-op18-no1-1": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No1/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no1_mov1.mxl",
    ),
    "abc-op18-no1-2": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No1/2/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no1_mov2.mxl",
    ),
    "abc-op18-no1-3": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No1/3/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no1_mov3.mxl",
    ),
    "abc-op18-no1-4": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No1/4/analysis.txt",
        "AlignedABC/op18_no1_mov4.mxl",
    ),
    "abc-op18-no2-1": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No2/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no2_mov1.mxl",
    ),
    "abc-op18-no2-2": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No2/2/analysis.txt",
        "AlignedABC/op18_no2_mov2.mxl",
    ),
    "abc-op18-no2-3": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No2/3/analysis.txt",
        "AlignedABC/op18_no2_mov3.mxl",
    ),
    "abc-op18-no2-4": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No2/4/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no2_mov4.mxl",
    ),
    "abc-op18-no3-1": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No3/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no3_mov1.mxl",
    ),
    "abc-op18-no3-2": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No3/2/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no3_mov2.mxl",
    ),
    "abc-op18-no3-3": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No3/3/analysis.txt",
        "AlignedABC/op18_no3_mov3.mxl",
    ),
    "abc-op18-no3-4": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No3/4/analysis.txt",
        "AlignedABC/op18_no3_mov4.mxl",
    ),
    "abc-op18-no4-1": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No4/1/analysis.txt",
        "AlignedABC/op18_no4_mov1.mxl",
    ),
    "abc-op18-no4-2": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No4/2/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no4_mov2.mxl",
    ),
    "abc-op18-no4-3": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No4/3/analysis.txt",
        "AlignedABC/op18_no4_mov3.mxl",
    ),
    "abc-op18-no4-4": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No4/4/analysis.txt",
        "AlignedABC/op18_no4_mov4.mxl",
    ),
    "abc-op18-no5-1": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No5/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no5_mov1.mxl",
    ),
    "abc-op18-no5-2": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No5/2/analysis.txt",
        "AlignedABC/op18_no5_mov2.mxl",
    ),
    "abc-op18-no5-3": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No5/3/analysis.txt",
        "AlignedABC/op18_no5_mov3.mxl",
    ),
    "abc-op18-no5-4": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No5/4/analysis.txt",
        "AlignedABC/op18_no5_mov4.mxl",
    ),
    "abc-op18-no6-1": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No6/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no6_mov1.mxl",
    ),
    "abc-op18-no6-2": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No6/2/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op18_no6_mov2.mxl",
    ),
    "abc-op18-no6-3": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No6/3/analysis.txt",
        "AlignedABC/op18_no6_mov3.mxl",
    ),
    "abc-op18-no6-4": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op18_No6/4/analysis.txt",
        "AlignedABC/op18_no6_mov4.mxl",
    ),
    "abc-op59-no1-1": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No1/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no7_mov1.mxl",
    ),
    "abc-op59-no1-2": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No1/2/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no7_mov2.mxl",
    ),
    "abc-op59-no1-3": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No1/3/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no7_mov3.mxl",
    ),
    "abc-op59-no1-4": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No1/4/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no7_mov4.mxl",
    ),
    "abc-op59-no2-1": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No2/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no8_mov1.mxl",
    ),
    "abc-op59-no2-2": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No2/2/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no8_mov2.mxl",
    ),
    "abc-op59-no2-3": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No2/3/analysis.txt",
        "AlignedABC/op59_no8_mov3.mxl",
    ),
    "abc-op59-no2-4": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No2/4/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no8_mov4.mxl",
    ),
    "abc-op59-no3-1": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No3/1/analysis.txt",
        "AlignedABC/op59_no9_mov1.mxl",
    ),
    "abc-op59-no3-2": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No3/2/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no9_mov2.mxl",
    ),
    "abc-op59-no3-3": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No3/3/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op59_no9_mov3.mxl",
    ),
    "abc-op59-no3-4": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op59_No3/4/analysis.txt",
        "AlignedABC/op59_no9_mov4.mxl",
    ),
    "abc-op74-1": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op74/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op74_no10_mov1.mxl",
    ),
    "abc-op74-2": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op74/2/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op74_no10_mov2.mxl",
    ),
    "abc-op74-3": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op74/3/analysis.txt",
        "AlignedABC/op74_no10_mov3.mxl",
    ),
    "abc-op74-4": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op74/4/analysis.txt",
        "AlignedABC/op74_no10_mov4.mxl",
    ),
    "abc-op95-1": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op95/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op95_no11_mov1.mxl",
    ),
    "abc-op95-2": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op95/2/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op95_no11_mov2.mxl",
    ),
    "abc-op95-3": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op95/3/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op95_no11_mov3.mxl",
    ),
    "abc-op95-4": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op95/4/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op95_no11_mov4.mxl",
    ),
    "abc-op127-1": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op127/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op127_no12_mov1.mxl",
    ),
    "abc-op127-2": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op127/2/analysis.txt",
        "AlignedABC/op127_no12_mov2.mxl",
    ),
    "abc-op127-3": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op127/3/analysis.txt",
        "AlignedABC/op127_no12_mov3.mxl",
    ),
    "abc-op127-4": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op127/4/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op127_no12_mov4.mxl",
    ),
    "abc-op130-1": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op130/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op130_no13_mov1.mxl",
    ),
    "abc-op130-2": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op130/2/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op130_no13_mov2.mxl",
    ),
    "abc-op130-3": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op130/3/analysis.txt",
        "AlignedABC/op130_no13_mov3.mxl",
    ),
    "abc-op130-4": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op130/4/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op130_no13_mov4.mxl",
    ),
    "abc-op130-5": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op130/5/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op130_no13_mov5.mxl",
    ),
    "abc-op130-6": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op130/6/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op130_no13_mov6.mxl",
    ),
    "abc-op131-1": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op131_no14_mov1.mxl",
    ),
    "abc-op131-2": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/2/analysis.txt",
        "AlignedABC/op131_no14_mov2.mxl",
    ),
    "abc-op131-3": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/3/analysis.txt",
        "AlignedABC/op131_no14_mov3.mxl",
    ),
    "abc-op131-4": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/4/analysis.txt",
        "AlignedABC/op131_no14_mov4.mxl",
    ),
    "abc-op131-5": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/5/analysis.txt",
        "AlignedABC/op131_no14_mov5.mxl",
    ),
    "abc-op131-6": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/6/analysis.txt",
        "AlignedABC/op131_no14_mov6.mxl",
    ),
    "abc-op131-7": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op131/7/analysis.txt",
        "AlignedABC/op131_no14_mov7.mxl",
    ),
    "abc-op132-1": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op132/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op132_no15_mov1.mxl",
    ),
    "abc-op132-2": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op132/2/analysis.txt",
        "AlignedABC/op132_no15_mov2.mxl",
    ),
    "abc-op132-3": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op132/3/analysis.txt",
        "AlignedABC/op132_no15_mov3.mxl",
    ),
    "abc-op132-4": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op132/4/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op132_no15_mov4.mxl",
    ),
    "abc-op132-5": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op132/5/analysis.txt",
        "AlignedABC/op132_no15_mov5.mxl",
    ),
    "abc-op135-1": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op135/1/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op135_no16_mov1.mxl",
    ),
    "abc-op135-2": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op135/2/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op135_no16_mov2.mxl",
    ),
    "abc-op135-3": (
        "When-in-Rome/Corpus/Quartets/Beethoven,_Ludwig_van/Op135/3/analysis.txt",
        "functional-harmony-micchi/data/Beethoven_4tets/scores/op135_no16_mov3.mxl",
    ),
    "abc-op135-4": (
        "AlignedWiR/Corpus/Quartets/Beethoven,_Ludwig_van/Op135/4/analysis.txt",
        "AlignedABC/op135_no16_mov4.mxl",
    ),
    "haydnop20-no1-1": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No1/1/analysis.txt",
        "haydn_op20_harm/op20/1/i/op20n1-01.krn",
    ),
    "haydnop20-no1-2": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No1/2/analysis.txt",
        "haydn_op20_harm/op20/1/ii/op20n1-02.krn",
    ),
    "haydnop20-no1-3": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No1/3/analysis.txt",
        "haydn_op20_harm/op20/1/iii/op20n1-03.krn",
    ),
    "haydnop20-no1-4": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No1/4/analysis.txt",
        "haydn_op20_harm/op20/1/iv/op20n1-04.krn",
    ),
    "haydnop20-no2-1": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No2/1/analysis.txt",
        "haydn_op20_harm/op20/2/i/op20n2-01.krn",
    ),
    "haydnop20-no2-2": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No2/2/analysis.txt",
        "haydn_op20_harm/op20/2/ii/op20n2-02.krn",
    ),
    "haydnop20-no2-3": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No2/3/analysis.txt",
        "haydn_op20_harm/op20/2/iii/op20n2-03.krn",
    ),
    "haydnop20-no2-4": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No2/4/analysis.txt",
        "haydn_op20_harm/op20/2/iv/op20n2-04.krn",
    ),
    "haydnop20-no3-1": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No3/1/analysis.txt",
        "haydn_op20_harm/op20/3/i/op20n3-01.krn",
    ),
    "haydnop20-no3-2": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No3/2/analysis.txt",
        "haydn_op20_harm/op20/3/ii/op20n3-02.krn",
    ),
    "haydnop20-no3-3": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No3/3/analysis.txt",
        "haydn_op20_harm/op20/3/iii/op20n3-03.krn",
    ),
    "haydnop20-no3-4": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No3/4/analysis.txt",
        "haydn_op20_harm/op20/3/iv/op20n3-04.krn",
    ),
    "haydnop20-no4-1": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No4/1/analysis.txt",
        "haydn_op20_harm/op20/4/i/op20n4-01.krn",
    ),
    "haydnop20-no4-2": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No4/2/analysis.txt",
        "haydn_op20_harm/op20/4/ii/op20n4-02.krn",
    ),
    "haydnop20-no4-3": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No4/3/analysis.txt",
        "haydn_op20_harm/op20/4/iii/op20n4-03.krn",
    ),
    "haydnop20-no4-4": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No4/4/analysis.txt",
        "haydn_op20_harm/op20/4/iv/op20n4-04.krn",
    ),
    "haydnop20-no5-1": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No5/1/analysis.txt",
        "haydn_op20_harm/op20/5/i/op20n5-01.krn",
    ),
    "haydnop20-no5-2": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No5/2/analysis.txt",
        "haydn_op20_harm/op20/5/ii/op20n5-02.krn",
    ),
    "haydnop20-no5-3": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No5/3/analysis.txt",
        "haydn_op20_harm/op20/5/iii/op20n5-03.krn",
    ),
    "haydnop20-no5-4": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No5/4/analysis.txt",
        "haydn_op20_harm/op20/5/iv/op20n5-04.krn",
    ),
    "haydnop20-no6-1": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No6/1/analysis.txt",
        "haydn_op20_harm/op20/6/i/op20n6-01.krn",
    ),
    "haydnop20-no6-2": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No6/2/analysis.txt",
        "haydn_op20_harm/op20/6/ii/op20n6-02.krn",
    ),
    "haydnop20-no6-3": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No6/3/analysis.txt",
        "haydn_op20_harm/op20/6/iii/op20n6-03.krn",
    ),
    "haydnop20-no6-4": (
        "When-in-Rome/Corpus/Quartets/Haydn,_Franz_Joseph/Op20_No6/4/analysis.txt",
        "haydn_op20_harm/op20/6/iv/op20n6-04.krn",
    ),
    "wir-orchestral-haydn-symphony-104-1": (
        "When-in-Rome/Corpus/Orchestral/Haydn,_Franz_Joseph/Symphony_104/1/analysis.txt",
        "When-in-Rome/Corpus/Orchestral/Haydn,_Franz_Joseph/Symphony_104/1/score.mxl",
    ),
}

DATASPLITS = {
    "test": [
        "abc-op74-3",
        "abc-op127-2",
        "abc-op95-3",
        "abc-op18-no6-3",
        "abc-op59-no1-1",
        "abc-op18-no1-3",
        "abc-op135-2",
        "abc-op59-no2-3",
        "abc-op18-no1-1",
        "abc-op74-4",
        "tavern-beethoven-woo-77-a",
        "tavern-beethoven-woo-77-b",
        "tavern-beethoven-woo-75-a",
        "tavern-beethoven-woo-75-b",
        "tavern-beethoven-woo-78-a",
        "tavern-beethoven-woo-78-b",
        "tavern-beethoven-woo-70-a",
        "tavern-beethoven-woo-70-b",
        "haydnop20-no2-2",
        "haydnop20-no3-4",
        "haydnop20-no5-3",
        "haydnop20-no6-4",
        "bps-01-op002-no1-1",
        "bps-14-op027-no2-moonlight-1",
        "bps-23-op057-appassionata-1",
        "bps-15-op028-pastorale-1",
        "bps-10-op014-no2-1",
        "bps-25-op079-sonatina-1",
        "bps-07-op010-no3-1",
        "wir-openscore-liedercorpus-schubert-die-schone-mullerin-d-795-12-pause",
        "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-08-der-atlas",
        "wir-openscore-liedercorpus-wolf-eichendorff-lieder-14-der-verzweifelte-liebhaber",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-16-die-alten-bosen-lieder",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-10-hor-ich-das-liedchen-klingen",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-04-wenn-ich-in-deine-augen-seh",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-03-gefrorne-thranen",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-12-am-leuchtenden-sommermorgen",
        "wir-openscore-liedercorpus-wolf-eichendorff-lieder-19-die-nacht",
        "wir-openscore-liedercorpus-reichardt-sechs-lieder-von-novalis-op-4-5-noch-ein-bergmannslied",
        "wir-openscore-liedercorpus-hensel-6-lieder-op-9-1-die-ersehnte",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-02-aus-meinen-tranen-spriessen",
        "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-05-aufenthalt",
        "wir-openscore-liedercorpus-schubert-op-59-3-du-bist-die-ruh",
        "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-10-das-fischermadchen",
        "wir-bach-wtc-i-24",
        "wir-bach-wtc-i-15",
        "wir-bach-wtc-i-8",
        "wir-bach-wtc-i-3",
        "wir-bach-chorales-19",
        "wir-bach-chorales-4",
        "wir-bach-chorales-10",
        "wir-monteverdi-madrigals-book-3-9",
        "wir-monteverdi-madrigals-book-5-7",
        "wir-monteverdi-madrigals-book-5-5",
    ],
    "validation": [
        "abc-op131-1",
        "abc-op59-no3-1",
        "abc-op59-no1-4",
        "abc-op18-no1-2",
        "abc-op18-no2-1",
        "abc-op131-4",
        "abc-op132-5",
        "abc-op18-no6-1",
        "abc-op59-no3-3",
        "abc-op18-no3-3",
        "tavern-mozart-k501-a",
        "tavern-mozart-k501-b",
        "tavern-beethoven-woo-64-a",
        "tavern-beethoven-woo-64-b",
        "tavern-mozart-k455-a",
        "tavern-mozart-k455-b",
        "tavern-beethoven-woo-80-a",
        "tavern-beethoven-woo-80-b",
        "haydnop20-no1-2",
        "haydnop20-no2-4",
        "haydnop20-no3-3",
        "haydnop20-no5-2",
        "bps-08-op013-pathetique-1",
        "bps-19-op049-no1-1",
        "bps-29-op106-hammerklavier-1",
        "bps-16-op031-no1-1",
        "bps-26-op081a-les-adieux-1",
        "bps-06-op010-no2-1",
        "bps-20-op049-no2-1",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-13-ich-hab-im-traum-geweinet",
        "wir-openscore-liedercorpus-hensel-6-lieder-op-9-5-der-maiabend",
        "wir-openscore-liedercorpus-brahms-6-songs-op-3-3-liebe-und-fruhling-ii",
        "wir-openscore-liedercorpus-hensel-6-lieder-op-9-3-der-rosenkranz",
        "wir-openscore-liedercorpus-wolf-eichendorff-lieder-08-nachtzauber",
        "wir-openscore-liedercorpus-hensel-6-lieder-op-9-4-die-fruhen-graber",
        "wir-openscore-liedercorpus-mahler-kindertotenlieder-2-nun-seh-ich-wohl-warum-so-dunkle-flammen",
        "wir-openscore-liedercorpus-schumann-6-lieder-op-13-3-liebeszauber",
        "wir-openscore-liedercorpus-schubert-4-lieder-op-96-1-die-sterne-d-939",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-11-fruhlingstraum",
        "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-07-abschied",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-22-muth",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-01-im-wunderschonen-monat-mai",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-18-der-stuermische-morgen",
        "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-13-der-doppelganger",
        "wir-bach-wtc-i-7",
        "wir-bach-wtc-i-17",
        "wir-bach-wtc-i-16",
        "wir-bach-wtc-i-11",
        "wir-bach-chorales-2",
        "wir-bach-chorales-14",
        "wir-bach-chorales-16",
        "wir-monteverdi-madrigals-book-3-10",
        "wir-monteverdi-madrigals-book-3-15",
        "wir-monteverdi-madrigals-book-3-13",
    ],
    "training": [
        "abc-op131-3",
        "abc-op95-4",
        "abc-op132-2",
        "abc-op95-2",
        "abc-op130-1",
        "abc-op95-1",
        "abc-op127-3",
        "abc-op18-no6-2",
        "abc-op127-4",
        "abc-op130-2",
        "abc-op18-no5-3",
        "abc-op59-no1-2",
        "abc-op59-no1-3",
        "abc-op18-no4-4",
        "abc-op18-no5-1",
        "abc-op132-1",
        "abc-op74-2",
        "abc-op18-no5-2",
        "abc-op127-1",
        "abc-op18-no3-2",
        "abc-op18-no2-4",
        "abc-op131-6",
        "abc-op135-4",
        "abc-op135-3",
        "abc-op18-no2-3",
        "abc-op18-no6-4",
        "abc-op59-no3-2",
        "abc-op59-no3-4",
        "abc-op59-no2-1",
        "abc-op18-no3-4",
        "abc-op18-no4-1",
        "abc-op131-7",
        "abc-op18-no2-2",
        "abc-op130-6",
        "abc-op130-5",
        "abc-op18-no4-3",
        "abc-op18-no3-1",
        "abc-op59-no2-2",
        "abc-op59-no2-4",
        "abc-op18-no4-2",
        "abc-op135-1",
        "abc-op18-no1-4",
        "abc-op132-4",
        "abc-op18-no5-4",
        "abc-op130-4",
        "abc-op131-2",
        "abc-op74-1",
        "abc-op132-3",
        "abc-op130-3",
        "abc-op131-5",
        "tavern-mozart-k353-a",
        "tavern-mozart-k353-b",
        "tavern-mozart-k265-a",
        "tavern-mozart-k265-b",
        "tavern-beethoven-woo-73-a",
        "tavern-beethoven-woo-73-b",
        "tavern-beethoven-op34-a",
        "tavern-beethoven-op34-b",
        "tavern-mozart-k025-a",
        "tavern-mozart-k025-b",
        "tavern-beethoven-woo-63-a",
        "tavern-beethoven-woo-63-b",
        "tavern-beethoven-woo-68-a",
        "tavern-beethoven-woo-68-b",
        "tavern-beethoven-woo-66-a",
        "tavern-beethoven-woo-66-b",
        "tavern-mozart-k398-a",
        "tavern-mozart-k398-b",
        "tavern-beethoven-woo-69-a",
        "tavern-beethoven-woo-69-b",
        "tavern-mozart-k573-a",
        "tavern-mozart-k573-b",
        "tavern-beethoven-woo-76-a",
        "tavern-beethoven-woo-76-b",
        "tavern-beethoven-woo-72-a",
        "tavern-beethoven-woo-72-b",
        "tavern-mozart-k613-a",
        "tavern-mozart-k613-b",
        "tavern-beethoven-woo-65-a",
        "tavern-beethoven-woo-65-b",
        "tavern-beethoven-op76-a",
        "tavern-beethoven-op76-b",
        "tavern-mozart-k179-a",
        "tavern-mozart-k179-b",
        "tavern-mozart-k354-a",
        "tavern-mozart-k354-b",
        "tavern-beethoven-woo-71-a",
        "tavern-beethoven-woo-71-b",
        "haydnop20-no6-3",
        "haydnop20-no1-1",
        "haydnop20-no4-1",
        "haydnop20-no4-3",
        "haydnop20-no1-3",
        "haydnop20-no6-2",
        "haydnop20-no3-1",
        "haydnop20-no5-1",
        "haydnop20-no1-4",
        "haydnop20-no2-3",
        "haydnop20-no5-4",
        "haydnop20-no3-2",
        "haydnop20-no4-4",
        "haydnop20-no2-1",
        "haydnop20-no4-2",
        "haydnop20-no6-1",
        "bps-02-op002-no2-1",
        "bps-03-op002-no3-1",
        "bps-04-op007-1",
        "bps-05-op010-no1-1",
        "bps-09-op014-no1-1",
        "bps-11-op022-1",
        "bps-12-op026-1",
        "bps-13-op027-no1-1",
        "bps-17-op031-no2-1",
        "bps-18-op031-no3-1",
        "bps-21-op053-1",
        "bps-22-op054-1",
        "bps-24-op078-1",
        "bps-27-op090-1",
        "bps-28-op101-1",
        "bps-30-op109-1",
        "bps-31-op110-1",
        "bps-32-op111-1",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-07-auf-dem-flusse",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-12-einsamkeit-urspruengliche-fassung",
        "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-12-am-meer",
        "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-07-die-wiese",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-16-letzte-hoffnung",
        "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-02-der-traurige-wanderer",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-15-aus-alten-marchen-winkt-es",
        "wir-openscore-liedercorpus-hensel-6-lieder-op-1-3-warum-sind-denn-die-rosen-so-blass",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-23-die-nebensonnen",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-05-der-lindenbaum",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-11-ein-jungling-liebt-ein-madchen",
        "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-03-die-blume-der-blumen",
        "wir-openscore-liedercorpus-wolf-eichendorff-lieder-15-unfall",
        "wir-openscore-liedercorpus-schumann-6-lieder-op-13-1-ich-stand-in-dunklen-traumen",
        "wir-openscore-liedercorpus-hensel-6-lieder-op-1-4-mayenlied",
        "wir-openscore-liedercorpus-schumann-frauenliebe-und-leben-op-42-1-seit-ich-ihn-gesehen",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-09-irrlicht",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-13-die-post",
        "wir-openscore-liedercorpus-chausson-7-melodies-op-2-7-le-colibri",
        "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-09-ihr-bild",
        "wir-openscore-liedercorpus-chaminade-amoroso",
        "wir-openscore-liedercorpus-hensel-3-lieder-1-sehnsucht",
        "wir-openscore-liedercorpus-wolf-eichendorff-lieder-13-der-scholar",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-14-der-greise-kopf",
        "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-09-hier-liegt-ein-spielmann-begraben",
        "wir-openscore-liedercorpus-hensel-6-lieder-op-1-1-schwanenlied",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-09-das-ist-ein-floten-und-geigen",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-05-ich-will-meine-seele-tauchen",
        "wir-openscore-liedercorpus-wolf-eichendorff-lieder-04-das-standchen",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-24-der-leiermann-spatere-fassung",
        "wir-openscore-liedercorpus-hensel-5-lieder-op-10-3-abendbild",
        "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-08-kaeuzlein",
        "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-05-betteley-der-vogel",
        "wir-openscore-liedercorpus-hensel-5-lieder-op-10-5-bergeslust",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-17-im-dorfe",
        "wir-openscore-liedercorpus-coleridge-taylor-oh-the-summer",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-02-die-wetterfahne",
        "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-03-fruhlingssehnsucht",
        "wir-openscore-liedercorpus-lang-6-lieder-op-25-4-lied-immer-sich-rein-kindlich-erfreun",
        "wir-openscore-liedercorpus-hensel-6-lieder-op-9-2-ferne",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-20-der-wegweiser",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-14-allnachtlich-im-traume",
        "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-14-die-taubenpost",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-19-tauschung",
        "wir-openscore-liedercorpus-schumann-6-lieder-op-13-6-die-stille-lotosblume",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-15-die-kraehe",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-08-ruckblick",
        "wir-openscore-liedercorpus-hensel-5-lieder-op-10-4-im-herbste",
        "wir-openscore-liedercorpus-franz-6-gesange-op-14-5-liebesfruhling",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-03-die-rose-die-lilie",
        "wir-openscore-liedercorpus-mahler-kindertotenlieder-4-oft-denk-ich-sie-sind-nur-ausgegangen",
        "wir-openscore-liedercorpus-hensel-5-lieder-op-10-2-vorwurf",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-21-das-wirthshaus",
        "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-06-in-der-ferne",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-07-ich-grolle-nicht",
        "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-11-die-stadt",
        "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-01-fruhlingsblumen",
        "wir-openscore-liedercorpus-hensel-5-lieder-op-10-1-nach-suden",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-10-rast-spatere-fassung",
        "wir-openscore-liedercorpus-wolf-eichendorff-lieder-20-waldmadchen",
        "wir-openscore-liedercorpus-reichardt-zwolf-deutsche-und-italianische-romantische-gesange-10-ida-aus-ariels-offenbarungen",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-08-und-wusstens-die-blumen",
        "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-04-wachtelwacht",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-04-erstarrung",
        "wir-openscore-liedercorpus-schubert-schwanengesang-d-957-02-kriegers-ahnung",
        "wir-openscore-liedercorpus-holmes-les-heures-4-lheure-dazur",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-06-wasserfluth",
        "wir-openscore-liedercorpus-schumann-die-gute-nacht",
        "wir-openscore-liedercorpus-schumann-dichterliebe-op-48-06-im-rhein-im-heiligen-strome",
        "wir-openscore-liedercorpus-schumann-frauenliebe-und-leben-op-42-3-ich-kanns-nicht-fassen",
        "wir-openscore-liedercorpus-jaell-4-melodies-1-a-toi",
        "wir-openscore-liedercorpus-schumann-lieder-op-12-04-liebst-du-um-schonheit",
        "wir-openscore-liedercorpus-schumann-6-lieder-op-13-2-sie-liebten-sich-beide",
        "wir-openscore-liedercorpus-hensel-6-lieder-op-1-6-gondellied",
        "wir-openscore-liedercorpus-schubert-winterreise-d-911-01-gute-nacht",
        "wir-openscore-liedercorpus-hensel-6-lieder-op-1-5-morgenstandchen",
        "wir-openscore-liedercorpus-brahms-7-lieder-op-48-3-liebesklage-des-madchens",
        "wir-bach-wtc-i-20",
        "wir-bach-wtc-i-19",
        "wir-bach-wtc-i-22",
        "wir-bach-wtc-i-9",
        "wir-bach-wtc-i-18",
        "wir-bach-wtc-i-1",
        "wir-bach-wtc-i-5",
        "wir-bach-wtc-i-4",
        "wir-bach-wtc-i-6",
        "wir-bach-wtc-i-10",
        "wir-bach-wtc-i-14",
        "wir-bach-wtc-i-23",
        "wir-bach-wtc-i-2",
        "wir-bach-wtc-i-21",
        "wir-bach-wtc-i-12",
        "wir-bach-wtc-i-13",
        "wir-bach-chorales-6",
        "wir-bach-chorales-18",
        "wir-bach-chorales-3",
        "wir-bach-chorales-9",
        "wir-bach-chorales-12",
        "wir-bach-chorales-7",
        "wir-bach-chorales-5",
        "wir-bach-chorales-20",
        "wir-bach-chorales-1",
        "wir-bach-chorales-17",
        "wir-bach-chorales-13",
        "wir-bach-chorales-8",
        "wir-monteverdi-madrigals-book-3-14",
        "wir-monteverdi-madrigals-book-3-6",
        "wir-monteverdi-madrigals-book-3-11",
        "wir-monteverdi-madrigals-book-3-19",
        "wir-monteverdi-madrigals-book-3-8",
        "wir-monteverdi-madrigals-book-3-3",
        "wir-monteverdi-madrigals-book-4-11",
        "wir-monteverdi-madrigals-book-4-12",
        "wir-monteverdi-madrigals-book-5-4",
        "wir-monteverdi-madrigals-book-4-19",
        "wir-monteverdi-madrigals-book-4-13",
        "wir-monteverdi-madrigals-book-4-10",
        "wir-monteverdi-madrigals-book-5-8",
        "wir-monteverdi-madrigals-book-3-1",
        "wir-variations-and-grounds-bach-b-minor-mass-bwv232-crucifixus",
        "wir-variations-and-grounds-purcell-sonata-z807",
        "wir-variations-and-grounds-purcell-chacony-z730",
        "wir-orchestral-haydn-symphony-104-1",
    ],
}