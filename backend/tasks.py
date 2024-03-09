from celery_app import celery_app
from src.analysis import Analyser


@celery_app.task(track_started=True, max_retries=2)
def analyse(
    sample_characteristics: dict,
    phenotype: str,
    cpg: str,
    rs: str,
) -> dict:
    analysis = Analyser(
        sample_characteristics, cpg, rs, phenotype
    )
    analysis.load_omics_data()
    analysis.load_pheno_data()

    plot_mqtl = analysis.categorical_plot(analysis.cpg, (0, 1))
    plot_genotype_freq = analysis.plot_genotype_frequency()

    plot_phenotype_genotype = analysis.categorical_plot(analysis.phenotype)
    plot_phenotype_genotype_methyltype = analysis.scatter_plot()

    table_a, table_b = analysis.model()
    table_c = analysis.genotype_phenotype_assoc()
    table_d = analysis.methyltype_phenotype_assoc()

    return {
        "tableA": table_a,
        "tableB": table_b,
        "mqtl_plot": plot_mqtl,
        "genotype_frequency_plot": plot_genotype_freq,
        "tableC": table_c,
        "tableD": table_d,
        "phenotype_genotype_plot": plot_phenotype_genotype,
        "phenotype_genotype_methyltype_plot": plot_phenotype_genotype_methyltype,
    }
