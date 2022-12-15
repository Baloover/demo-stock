from infrastucture.scheduler import SchedulerApp, DataGenerationJob
from modules.stock_data_generator import StockData
from settings import TICKERS_LIST
from apscheduler.triggers.cron import CronTrigger


app = SchedulerApp(
    title="Stock data producer"
)


@app.get("/ping")
async def ping():
    return


@app.get("/health")
async def health():
    return {"message": "Hello World"}


@app.get("/status")
async def status():
    return {"message": "Hello World"}


@app.on_event('startup')
async def startup_producers():
    app.initialize_scheduler()
    for ticker in TICKERS_LIST:
        job = DataGenerationJob(str(ticker), StockData(ticker=str(ticker)))
        app.job_store.append(job)
        app.scheduler.add_job(app.execute,
                              trigger=CronTrigger(second='*'),
                              id=job.ticker,
                              kwargs={
                                    'callback': job.data_generator.generate_point,
                                    'timeout': 2,
                                })
    app.start_scheduler()


@app.on_event('shutdown')
async def shutdown_consumers():
    await app.stop_scheduler()
