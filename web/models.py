from django.db import models

# Create your models here.

# vcRNAdb


class data(models.Model):
    Id = models.AutoField(primary_key=True)
    Circ_id = models.CharField(max_length=40)
    Name = models.CharField(max_length=100)
    Virus = models.CharField(max_length=20)
    Genome = models.CharField(max_length=15)
    Genome_length = models.IntegerField()
    Splice_start = models.IntegerField()
    Splice_end = models.IntegerField()
    Splice_length = models.IntegerField()
    Strand = models.CharField(max_length=30)
    Annotation_region = models.CharField(max_length=500)
    Annotation_gene = models.CharField(max_length=500)
    Annotation_type = models.CharField(max_length=20)
    Cancer = models.CharField(max_length=50)
    Supported_samples = models.IntegerField()
    Supported_reads = models.IntegerField()
    Avg_CPM = models.FloatField()
    # Per-sample CPM values, semicolon-separated (one entry per supporting sample).
    CPM = models.CharField(max_length=1000)
    Avg_junction_reads = models.FloatField()
    # Sample_reads = models.CharField(max_length=100)
    # Sum_ratio = models.FloatField()
    # Evidence_score = models.FloatField()
    # PMER = models.FloatField()
    Junction_reads = models.CharField(max_length=200)
    # Non_junction_reads = models.CharField(max_length=200)
    # Junction_reads_ratio = models.CharField(max_length=200)
    Sample = models.CharField(max_length=400)
    # GEO_title = models.CharField(max_length=200)
    Study = models.CharField(max_length=200)
    Study_run = models.CharField(max_length=200)
    Sequencing_type = models.CharField(max_length=100)
    Experiment_condition = models.CharField(max_length=200)
    PMID = models.CharField(max_length=50)
    Organism = models.CharField(max_length=20)
    Publication_title = models.CharField(max_length=200)


class downloadInfo(models.Model):
    Id = models.AutoField(primary_key=True)
    Mail = models.CharField(max_length=40)
    Date = models.DateTimeField(auto_now=True)

# dtdb


class dtdb(models.Model):
    Id = models.IntegerField(primary_key=True)
    Drug_id = models.IntegerField()
    Drug = models.CharField(max_length=50)
    Leaf_id = models.IntegerField()
    Split_score = models.FloatField()
    Is_leaf = models.BooleanField()
    Parent_id = models.IntegerField()
    Sample = models.CharField(max_length=10000)
    Category = models.CharField(max_length=10000)
    Category_median = models.FloatField()
    Type = models.CharField(max_length=20)
    Min_conc = models.FloatField()
    Max_conc = models.FloatField()
    Lineage = models.CharField(max_length=10000)
    Lineage_set = models.CharField(max_length=5000)


class dtdb_mut(models.Model):
    Id = models.IntegerField(primary_key=True)
    Gene = models.CharField(max_length=20)
    pval_chi2q_mutGroup = models.FloatField()  # 2group
    drug = models.CharField(max_length=50)
    nodes = models.CharField(max_length=50)
    ratios = models.CharField(max_length=250)
    pval_chi2q_twoGroup = models.CharField(max_length=500)  # each2group
    correlation_trend = models.CharField(max_length=20)
    direction = models.CharField(max_length=10)
    dir_corr = models.FloatField()
    dir_p = models.FloatField()
    dir_xl = models.CharField(max_length=10)
    xl = models.FloatField(null=True, blank=True)
    padj_chi2q_mutGroup = models.FloatField()  # 2group
    cancer_gene = models.CharField(max_length=5)


class dtdb_expr(models.Model):
    Id = models.IntegerField(primary_key=True)
    Gene = models.CharField(max_length=20)
    pval_ttest_2Group = models.FloatField()
    drug = models.CharField(max_length=50)
    nodes = models.CharField(max_length=50)
    ratios = models.CharField(max_length=250)  # expr median
    pval_u_eachTwoGroup = models.CharField(max_length=500)
    correlation_trend = models.CharField(max_length=20)
    direction = models.CharField(max_length=10)
    dir_corr = models.FloatField()
    dir_p = models.FloatField()
    sensi_drugCorr = models.FloatField()
    sensi_drugCorrP = models.FloatField()
    padj_ttest_mutGroup = models.FloatField()
    padj_sensi_drugCorr = models.FloatField()
    cancer_gene = models.CharField(max_length=5)


class dtdb_drug(models.Model):
    Id = models.IntegerField(primary_key=True)
    Drug_id = models.CharField(max_length=20)
    Screening_site = models.CharField(max_length=10)
    Drug_name = models.CharField(max_length=50)
    Synonyms = models.CharField(max_length=100)
    Target = models.CharField(max_length=50)
    Target_pathway = models.CharField(max_length=100)
    Expr_connect = models.CharField(max_length=10)
    Mut_connect = models.CharField(max_length=10)


class dtdb_drug_similarity(models.Model):
    Id = models.IntegerField(primary_key=True)
    drugId1 = models.CharField(max_length=20)
    drugName1 = models.CharField(max_length=50)
    drugId2 = models.CharField(max_length=20)
    similarity = models.FloatField()
    drugName2 = models.CharField(max_length=50)
    synonyms = models.CharField(max_length=100)
    target = models.CharField(max_length=50)
    targetPathway = models.CharField(max_length=100)


class dtdb_ccl_similarity(models.Model):
    Id = models.IntegerField(primary_key=True)
    ccl1 = models.CharField(max_length=20)
    ccl2 = models.CharField(max_length=20)
    similarity = models.FloatField(null=True, blank=True)
    ccl1name = models.CharField(max_length=20)
    ccl2name = models.CharField(max_length=20)
    TCGA = models.CharField(max_length=20)


class dtdb_ct_similarity(models.Model):
    Id = models.IntegerField(primary_key=True)
    ct = models.CharField(max_length=20)
    cluster = models.IntegerField()
    num = models.IntegerField()
    p = models.FloatField()


class dtdb_ct_similarity_cluster(models.Model):
    Id = models.IntegerField(primary_key=True)
    Cellline = models.CharField(max_length=20)
    Cluster = models.CharField(max_length=20)
    CosmicId = models.CharField(max_length=20)
    TCGAabbr = models.CharField(max_length=20)
