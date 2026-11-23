# Render queue

Scripts Bill has approved, in the order they should be made. The nightly production run takes the FIRST item with status `approved`, renders it, schedules it, and changes its status to `scheduled <date>`. Only Bill's picks go here.

<!-- Format:
## <idea id> — <title>
status: approved
script:
<one sentence per line, exactly as it should be voiced>
-->
