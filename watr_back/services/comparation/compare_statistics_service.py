from flask import abort

from auxiliary.compare_auxiliary.execute_compare_query import execute_compare_sparql_query
from auxiliary.compare_auxiliary.process_compare_output import process_compare_sparql_results


def compare_statistics_service(class_one, class_two):
    """
    Function that creates statistics for comparison.
    """
    try:
        output = execute_compare_sparql_query(class_one, class_two)
        result = process_compare_sparql_results(output, class_one, class_two)

        statistics = {
            class_one: {
                "properties": [],
                "total_count": 0,
                "most_used": None,
                "least_used": None,
                "unique_properties": []
            },
            class_two: {
                "properties": [],
                "total_count": 0,
                "most_used": None,
                "least_used": None,
                "unique_properties": []
            },
            "common_properties": []
        }

        # Track most & least used properties
        most_used_class_one = {"property": None, "count": -1}
        least_used_class_one = {"property": None, "count": float("inf")}
        most_used_class_two = {"property": None, "count": -1}
        least_used_class_two = {"property": None, "count": float("inf")}

        # Process results
        for row in result:
            prop = row["property"]
            count_one = int(row[class_one])
            count_two = int(row[class_two])

            # Track property lists
            if count_one > 0 and count_two > 0:
                statistics["common_properties"].append(prop)
                statistics[class_one]["properties"].append(prop)
                statistics[class_two]["properties"].append(prop)
            elif count_one > 0:
                statistics[class_one]["properties"].append(prop)
                statistics[class_one]["unique_properties"].append(prop)
            elif count_two > 0:
                statistics[class_two]["properties"].append(prop)
                statistics[class_two]["unique_properties"].append(prop)

            # Update most and least used for class_one
            if count_one > 0:
                if count_one > most_used_class_one["count"]:
                    most_used_class_one = {"property": prop, "count": count_one}
                if count_one < least_used_class_one["count"]:
                    least_used_class_one = {"property": prop, "count": count_one}

            # Update most and least used for class_two
            if count_two > 0:
                if count_two > most_used_class_two["count"]:
                    most_used_class_two = {"property": prop, "count": count_two}
                if count_two < least_used_class_two["count"]:
                    least_used_class_two = {"property": prop, "count": count_two}

        # Calculate total counts
        statistics[class_one]["total_count"] = len(statistics[class_one]["properties"])
        statistics[class_two]["total_count"] = len(statistics[class_two]["properties"])

        # Assign most/least used properties
        statistics[class_one]["most_used"] = most_used_class_one["property"]
        statistics[class_one]["least_used"] = least_used_class_one["property"]
        statistics[class_two]["most_used"] = most_used_class_two["property"]
        statistics[class_two]["least_used"] = least_used_class_two["property"]

        return statistics

    except Exception as e:
        return abort(500, f"An error occurred: {e}")
