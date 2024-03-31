#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
# import NewLabelBinarizer


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_risk.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    from loan_approval.NewLabelBinarizer import NewLabelBinarizer
    from loan_approval.node import Node
    from loan_approval import decision_tree
    # from loan_approval.random_forest import RandomForest    
    # from loan_approval.decision_tree import DecisionTree
    main()
