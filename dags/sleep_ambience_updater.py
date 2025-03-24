from airflow import DAG, macros
from airflow.operators.bash import BashOperator
from datetime import timedelta,datetime
import pendulum


default_args = {
    'owner' : 'john'
    ,'retries' : 5
    ,'retry_delay': timedelta(minutes=1)
}


with DAG(
    dag_id = 'weekly_sleep_ambience'
    ,description = 'this renders predefined rmarkdown reports weekly, and pushes them to a github.io project'
    ,start_date=datetime(2025,3,10,tzinfo=pendulum.timezone("America/Denver"))
    ,catchup = True
    ,schedule_interval = '00 9 * * 1'
) as dag:
    
    report_render = BashOperator(
        task_id = 'index_rmd'
        ,bash_command = "cd {{ var.value.r_dir_sleepAmb }}; Rscript renderer.R"
    )

    mv_results = BashOperator(
        task_id='mv_to_github'
        ,bash_command = "cd {{ var.value.r_dir_sleepAmb }}; mv -f index.md weeklyReport.html {{ var.value.githubIO_dir }}ambience_sleep/; mv -f images/*.png {{ var.value.githubIO_dir }}ambience_sleep/images/"
    )

    git_push = BashOperator(
        task_id = "update_githubIO"
        ,bash_command = "cd {{ var.value.githubIO_dir }}ambience_sleep/; git add index.md weeklyReport.html images/*.png; git commit -m 'updates results on {{ ds }}'; git push origin master"
    )

    report_render >> mv_results >> git_push 
