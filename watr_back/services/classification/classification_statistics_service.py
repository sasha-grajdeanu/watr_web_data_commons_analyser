from flask import abort

from auxiliary.classification_auxiliary.execute_classification_query import execute_classification_query
from auxiliary.classification_auxiliary.process_classification_output import process_classification_output


def classification_statistics_service(rdf_class, rdf_property):
    """
    Function that processes classification statistics.
    """
    try:
        output = execute_classification_query(rdf_class, rdf_property)
        results = process_classification_output(output)

        statistics = {
            "observations": [],
            "unique_subjects": {}
        }

        for result in results:
            subject = result.get("initial_subject")
            predicate = result.get("initial_predicate")
            levels = []

            for level in range(1, 4):
                level_predicate = result.get(f"level{level}_predicate")
                if level_predicate:
                    levels.append(level_predicate)
                else:
                    break

            statistics["observations"].append({
                "initialSubject": subject,
                "initialPredicate": predicate,
                "numberOfLevels": len(levels)
            })

            if subject not in statistics["unique_subjects"]:
                statistics["unique_subjects"][subject] = 0
            statistics["unique_subjects"][subject] += 1

        return statistics

    except Exception as e:
        return abort(500, f"An error occurred: {e}")
