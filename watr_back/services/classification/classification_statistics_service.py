from flask import abort

from auxiliary.classification_auxiliary.execute_classification_query import execute_classification_query
from auxiliary.classification_auxiliary.process_classification_output import process_classification_output


def classification_statistics_service(rdf_class, rdf_property):
    try:
        output = execute_classification_query(rdf_class, rdf_property)
        results = process_classification_output(output)

        statistics = {
            "observations": [],
            "unique_subjects": {},
            "depth_average": 0.0,
            "min_level": float('inf'),
            "max_level": float('inf'),
            "level_distribution":{
                "0_level": 0,
                "1_level": 0,
                "2_level": 0,
                "3_level": 0
            }
        }

        total_levels = 0
        total_observations = 0

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

            num_levels = len(levels)
            total_levels += num_levels
            total_observations += 1

            statistics["min_level"] = min(statistics["min_level"], num_levels) if statistics["min_level"] != float('inf') else num_levels
            statistics["max_level"] = max(statistics["max_level"], num_levels) if statistics["max_level"] != float('inf') else num_levels

            level_key = f"{num_levels}_level"
            if level_key in statistics["level_distribution"]:
                statistics["level_distribution"][level_key] += 1

            statistics["observations"].append({
                "initialSubject": subject,
                "initialPredicate": predicate,
                "numberOfLevels": len(levels)
            })

            if subject not in statistics["unique_subjects"]:
                statistics["unique_subjects"][subject] = 0
            statistics["unique_subjects"][subject] += 1

        if total_observations > 0:
            statistics["depth_average"] = total_levels / total_observations
        return statistics

    except Exception as e:
        return abort(500, f"An error occurred: {e}")
