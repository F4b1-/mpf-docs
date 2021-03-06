Device Control Events
=====================

Many devices in MPF have configuration options which lets them be
controlled via events. (These are called "device control events".) For
example, flippers and autofire coils have *enable_events* and
*disable_events*, shots have *enable_events*, *disable_events*, and
*reset_events*, shot groups have *enable_events*, *disable_events*,
*reset_events*, *rotate_right_events*, and *rotate_left_events*, etc.

You can specify these events in each device's settings on a machine-
wide basis in your machine config, and you can also specify these
events that are only active when a mode is active in your mode config
files. There are several options for how you specify these device
control events, depending on what you want to do.

If you have just one event
--------------------------

Even though these configuration entries use the word "events"
(plural), you can configure them for just one event. For example, if
you have a flipper device that you want to enable when a ball starts,
you can add the following line to the configuration for your flipper:

::

    enable_events: ball_started

If you have multiple events
---------------------------

If you want one of these actions to be performed based on any one of
multiple events, you can enter multiple events. For example, maybe you
want to disable a flipper when the ball ends, but you also want to
make sure it's disabled when a tilt or slam tilt event is posted. In
that case you'd enter your configuration like this:

::

    disable_events: ball_ending, tilt, slam_tilt

Note that in this case, the flipper will disable if *any* of these
events is posted. If you want to get fancy and require that multiple
events need to be posted before you disable your flipper, then you
would use an Accrual or Sequence Logic Block to track those events,
and then you'd add a new event to your ``events_when_complete:`` in that
Logic Block and then enter that same event in the ``disable_events:`` for
your flipper.

Note that when you're entering multiple events, you can
enter them all on the same line separated by commas, or you can enter
each one on its own line started with a dash and a space, like this:

::

    disable_events:
        - ball_ending
        - tilt
        - slam_tilt

It makes no difference to MPF, rather this is just a personal
preference for how you want your config files to look.

If you want to configure "delays" before performing your action
---------------------------------------------------------------

You can also enter delays (in either seconds or milliseconds) which
cause the enable, disable, or reset events to wait after one of your
events is fired. Here's an example from the "Solids" drop target bank
in Big Shot:

::

            reset_events:
                ball_starting: 0
                collect_special: .75s

In this case when the *ball_starting* event is posted, MPF will reset
the drop target group immediately (no delay, due to the "0" value), and
when the *collect_special* event is posted, MPF will wait 0.75 seconds
before resetting it. (So you see that different events can have
different delays.) In case you're wondering why we did this, take a
look at the reset_events configuration for the other bank of drop
targets (called "Stripes") in Big Shot:

::

            reset_events:
                ball_starting: 0.25s
                collect_special: 1s

If you look at these two sets of configurations together, you see that
when the *ball_starting* event is posted, MPF will reset the Solids
drop target bank immediately and then wait a quarter of a second
before resetting the Stripes drop target bank. We did this so that the
reset emulates the original characteristics of resetting one then the
other in succession, rather than resetting them both at the same time.

Also note that we have a similar quarter-second delay between the two
drop target banks when we reset them after the special is collected,
but in this case we reset them after 0.75 and 1 second. That's because
that collecting the special awards a replay which fires the knocker,
but if the knocker fires at the same time as the drop targets are
reset then the player can't hear the knocker since the drop target
reset coils in Big Shot are so massive. So when the special is
collected, we fire the knocker immediate, then 0.75 seconds later we
reset the Solids drop target bank, then 0.25 seconds after that we
reset the Stripes drop target bank.

You can enter these delay times in
either seconds or milliseconds, as outlined :doc:`here </config/instructions/time_strings>`.
All this is done via the config files with no custom Python code needed! :)
