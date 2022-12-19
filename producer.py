from infrastucture.kafka import KafkaProducer
from infrastucture.scheduler import SchedulerApp, DataGenerationJob
from modules.stock_data_generator import StockData
from settings import TICKERS_LIST, KAFKA_URL
from apscheduler.triggers.cron import CronTrigger
from pykafka import KafkaClient
from fastapi import Request


class StockDataProducer(SchedulerApp):
    kafka_client: KafkaClient = KafkaClient(KAFKA_URL)


app = StockDataProducer(
    title="Stock data producer"
)


@app.get("/ping")
async def ping():

    return


@app.get("/status")
async def status(request: Request):
    health_status = "healthy" if all(job.data_interface.is_healthy() for job in request.app.job_store) else "unhealthy"
    return {
        "total_jobs": len(request.app.job_store),
        "heath_status": health_status,
        "ticker_list": [job.ticker for job in request.app.job_store],
    }


@app.on_event('startup')
async def startup_producers():
    app.initialize_scheduler()
    for ticker in TICKERS_LIST:
        data_generator = StockData(ticker=ticker)
        job = DataGenerationJob(ticker,
                                data_generator.generate_point,
                                KafkaProducer(app.kafka_client, data_generator.get_ticker()))
        app.job_store.append(job)
        app.scheduler.add_job(app.execute,
                              trigger=CronTrigger(second='*'),
                              id=job.ticker,
                              kwargs={
                                  'callback': job,
                                  'timeout': 2,
                              })
    app.start_scheduler()


@app.on_event('shutdown')
async def shutdown_consumers():
    await app.stop_scheduler()
