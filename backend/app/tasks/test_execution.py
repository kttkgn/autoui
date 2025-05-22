from app.core.celery_app import celery_app
from app.services.test_executor import create_test_executor, execute_test_case
from app.core.logger import logger

@celery_app.task(name="execute_test_case")
def execute_test_case_task(test_case_id: int, device_id: str):
    """
    执行测试用例任务
    
    Args:
        test_case_id: 测试用例ID
        device_id: 设备ID
    """
    try:
        executor = create_test_executor(test_case_id, device_id)
        result = execute_test_case(executor)
        logger.info(f"测试用例执行完成: {test_case_id}")
        return result
    except Exception as e:
        logger.error(f"测试用例执行失败: {str(e)}")
        raise

@celery_app.task(name="generate_test_report")
def generate_test_report_task(execution_id: int):
    """
    生成测试报告任务
    
    Args:
        execution_id: 执行记录ID
    """
    try:
        executor = create_test_executor(execution_id=execution_id)
        report = executor.generate_report()
        logger.info(f"测试报告生成完成: {execution_id}")
        return report
    except Exception as e:
        logger.error(f"测试报告生成失败: {str(e)}")
        raise 