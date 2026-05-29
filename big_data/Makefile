.PHONY: check links placeholders curriculum projects assessments materials docs-build lab-l0 lab-l0-test lab-l1 lab-l1-test lab-l2 lab-l2-test lab-l3 lab-l3-test lab-l4 lab-l4-test lab-l5 lab-l5-test lab-test

check: links placeholders curriculum projects assessments

links:
	python3 scripts/check_links.py

placeholders:
	python3 scripts/check_placeholders.py

curriculum:
	python3 scripts/check_curriculum_refs.py

projects:
	python3 scripts/check_project_catalog.py

assessments:
	python3 scripts/validate_assessments.py

materials:
	python3 scripts/build_learner_quiz.py

docs-build:
	python3 scripts/build_docs_source.py
	mkdocs build

lab-l0:
	cd labs/l0-web-log-analysis && python3 generate_logs.py --rows 200 --output data/access.log
	cd labs/l0-web-log-analysis && python3 analyze_logs.py data/access.log --output output/report.json

lab-l0-test: lab-l0
	cd labs/l0-web-log-analysis && python3 -m unittest test_analyze_logs.py

lab-l1:
	cd labs/l1-sql-warehouse && python3 build_db.py --output data/ecommerce.db
	cd labs/l1-sql-warehouse && python3 run_analytics.py data/ecommerce.db --output output/report.json

lab-l1-test: lab-l1
	cd labs/l1-sql-warehouse && python3 -m unittest test_sql_warehouse.py

lab-l2:
	cd labs/l2-streaming-window && python3 generate_events.py --rows 240 --output data/events.jsonl
	cd labs/l2-streaming-window && python3 window_aggregate.py data/events.jsonl --output output/window_report.json

lab-l2-test: lab-l2
	cd labs/l2-streaming-window && python3 -m unittest test_streaming_window.py

lab-l3:
	cd labs/l3-skew-tuning && python3 generate_skewed_events.py --rows 5000 --output data/events.csv
	cd labs/l3-skew-tuning && python3 compare_strategies.py data/events.csv --output output/report.json

lab-l3-test: lab-l3
	cd labs/l3-skew-tuning && python3 -m unittest test_skew_tuning.py

lab-l4:
	cd labs/l4-architecture-scorecard && python3 score_architecture.py data/options.json --output output/decision.json

lab-l4-test: lab-l4
	cd labs/l4-architecture-scorecard && python3 -m unittest test_score_architecture.py

lab-l5:
	cd labs/l5-strategy-radar && python3 build_radar.py data/technologies.csv --output output/radar.json

lab-l5-test: lab-l5
	cd labs/l5-strategy-radar && python3 -m unittest test_strategy_radar.py

lab-test: lab-l0-test lab-l1-test lab-l2-test lab-l3-test lab-l4-test lab-l5-test
