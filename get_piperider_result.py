"""
get piperider test result
sample: python tmp.py \
            --json-file-path "/Users/benliu/Dev/github/ithome-data-transfer/output/demo/.piperider/outputs/latest/run.json" \
            --data-source-name "content_info"
"""
import click
import json


@click.command()
@click.option('--run-json-file', type=str, default='')
@click.option('--data-source-name', type=str, required=True)
def main(data_source_name: str, run_json_file: str) -> None:
    """extract piperider test result from run json
    Arguments:
        data_source_name: piperider data source name
        run_json_file: piperider out.json file path. deault value:
            output/{data_source_name}/.piperider/outputs/latest/run.json
    Raises:
        AssertionError: rasie when test result failed
    """
    if not run_json_file: 
        run_json_file = f'./output/{data_source_name}/.piperider/outputs/latest/run.json'
    run_json_data = json.load(open(run_json_file))
    test_result = run_json_data['tables'][data_source_name]['piperider_assertion_result']['columns']
    TEST_RESULT='succeed'
    error_msg_list = []

    for col, result in test_result.items():
        for test_item in result:
            if test_item['status'] != 'passed':
                error_msg_list.append(f'{col}: {test_item}')
                TEST_RESULT='failed'

    if TEST_RESULT == 'failed':
        raise AssertionError('\n'.join(error_msg_list))

if __name__ == "__main__":
    main()
