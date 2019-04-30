#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2016, Brian Coca <bcoca@ansible.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'core'}

DOCUMENTATION = '''
module: systemd
author:
    - Ansible Core Team
version_added: "2.2"
short_description:  Manage services
description:
    - Controls systemd services on remote hosts.
options:
    name:
        description:
            - Name of the service. When using in a chroot environment you always need to specify the full name i.e. (crond.service).
        aliases: [ service, unit ]
    state:
        description:
            - C(started)/C(stopped) are idempotent actions that will not run commands unless necessary.
              C(restarted) will always bounce the service. C(reloaded) will always reload.
              C(restarted) and C(reloaded) will start the service if it's not already started.
        choices: [ reloaded, restarted, started, stopped ]
    enabled:
        description:
            - Whether the service should start on boot. B(At least one of state and enabled are required.)
        type: bool
    force:
        description:
            - Whether to override existing symlinks.
        type: bool
        version_added: 2.6
    masked:
        description:
            - Whether the unit should be masked or not, a masked unit is impossible to start.
        type: bool
    daemon_reload:
        description:
            - Run daemon-reload before doing any other operations, to make sure systemd has read any changes.
            - When set to C(yes), runs daemon-reload even if the module does not start or stop anything.
        type: bool
        default: no
        aliases: [ daemon-reload ]
    daemon_reexec:
        description:
            - Run daemon_reexec command before doing any other operations, the systemd manager will serialize the manager state.
        type: bool
        default: no
        aliases: [ daemon-reexec ]
        version_added: "2.8"
    user:
        description:
            - (deprecated) run ``systemctl`` talking to the service manager of the calling user, rather than the service manager
              of the system.
            - This option is deprecated and will eventually be removed in 2.11. The ``scope`` option should be used instead.
        type: bool
        default: no
    scope:
        description:
            - run systemctl within a given service manager scope, either as the default system scope (system),
              the current user's scope (user), or the scope of all users (global).
            - "For systemd to work with (user), the executing user must have its own instance of dbus started (systemd requirement).
              The user dbus process is normally started during normal login, but not during the run of Ansible tasks.
              Otherwise you will probably get a 'Failed to connect to bus: no such file or directory' error."
            - "Beware, scope (global) is similar to scope (user) except for the (enabled) action.
              For exemple, (daemon_reload) with scope (global) will actually have the same effecte as with scope (user).
              Try it manually before filling bug."
        choices: [ system, user, global ]
        version_added: "2.7"
    no_block:
        description:
            - Do not synchronously wait for the requested operation to finish.
              Enqueued job will continue without Ansible blocking on its completion.
        type: bool
        default: no
        version_added: "2.3"
notes:
    - Since 2.4, one of the following options is required 'state', 'enabled', 'masked', 'daemon_reload', ('daemon_reexec' since 2.8),
      and all except 'daemon_reload' (and 'daemon_reexec' since 2.8) also require 'name'.
    - Before 2.4 you always required 'name'.
    - Globs are not supported in name, i.e ``postgres*.service``.
requirements:
    - A system managed by systemd.
'''

EXAMPLES = '''
- name: Make sure a service is running
  systemd:
    state: started
    name: httpd

- name: stop service cron on debian, if running
  systemd:
    name: cron
    state: stopped

- name: restart service cron on centos, in all cases, also issue daemon-reload to pick up config changes
  systemd:
    state: restarted
    daemon_reload: yes
    name: crond

- name: reload service httpd, in all cases
  systemd:
    name: httpd
    state: reloaded

- name: enable service httpd and ensure it is not masked
  systemd:
    name: httpd
    enabled: yes
    masked: no

- name: enable a timer for dnf-automatic
  systemd:
    name: dnf-automatic.timer
    state: started
    enabled: yes

- name: just force systemd to reread configs (2.4 and above)
  systemd:
    daemon_reload: yes

- name: just force systemd to re-execute itself (2.8 and above)
  systemd:
    daemon_reexec: yes
'''

RETURN = '''
status:
    description: A dictionary with the key=value pairs returned from `systemctl show`
    returned: success
    type: complex
    contains: {
            "ActiveEnterTimestamp": "Sun 2016-05-15 18:28:49 EDT",
            "ActiveEnterTimestampMonotonic": "8135942",
            "ActiveExitTimestampMonotonic": "0",
            "ActiveState": "active",
            "After": "auditd.service systemd-user-sessions.service time-sync.target systemd-journald.socket basic.target system.slice",
            "AllowIsolate": "no",
            "Before": "shutdown.target multi-user.target",
            "BlockIOAccounting": "no",
            "BlockIOWeight": "1000",
            "CPUAccounting": "no",
            "CPUSchedulingPolicy": "0",
            "CPUSchedulingPriority": "0",
            "CPUSchedulingResetOnFork": "no",
            "CPUShares": "1024",
            "CanIsolate": "no",
            "CanReload": "yes",
            "CanStart": "yes",
            "CanStop": "yes",
            "CapabilityBoundingSet": "18446744073709551615",
            "ConditionResult": "yes",
            "ConditionTimestamp": "Sun 2016-05-15 18:28:49 EDT",
            "ConditionTimestampMonotonic": "7902742",
            "Conflicts": "shutdown.target",
            "ControlGroup": "/system.slice/crond.service",
            "ControlPID": "0",
            "DefaultDependencies": "yes",
            "Delegate": "no",
            "Description": "Command Scheduler",
            "DevicePolicy": "auto",
            "EnvironmentFile": "/etc/sysconfig/crond (ignore_errors=no)",
            "ExecMainCode": "0",
            "ExecMainExitTimestampMonotonic": "0",
            "ExecMainPID": "595",
            "ExecMainStartTimestamp": "Sun 2016-05-15 18:28:49 EDT",
            "ExecMainStartTimestampMonotonic": "8134990",
            "ExecMainStatus": "0",
            "ExecReload": "{ path=/bin/kill ; argv[]=/bin/kill -HUP $MAINPID ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }",
            "ExecStart": "{ path=/usr/sbin/crond ; argv[]=/usr/sbin/crond -n $CRONDARGS ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }",
            "FragmentPath": "/usr/lib/systemd/system/crond.service",
            "GuessMainPID": "yes",
            "IOScheduling": "0",
            "Id": "crond.service",
            "IgnoreOnIsolate": "no",
            "IgnoreOnSnapshot": "no",
            "IgnoreSIGPIPE": "yes",
            "InactiveEnterTimestampMonotonic": "0",
            "InactiveExitTimestamp": "Sun 2016-05-15 18:28:49 EDT",
            "InactiveExitTimestampMonotonic": "8135942",
            "JobTimeoutUSec": "0",
            "KillMode": "process",
            "KillSignal": "15",
            "LimitAS": "18446744073709551615",
            "LimitCORE": "18446744073709551615",
            "LimitCPU": "18446744073709551615",
            "LimitDATA": "18446744073709551615",
            "LimitFSIZE": "18446744073709551615",
            "LimitLOCKS": "18446744073709551615",
            "LimitMEMLOCK": "65536",
            "LimitMSGQUEUE": "819200",
            "LimitNICE": "0",
            "LimitNOFILE": "4096",
            "LimitNPROC": "3902",
            "LimitRSS": "18446744073709551615",
            "LimitRTPRIO": "0",
            "LimitRTTIME": "18446744073709551615",
            "LimitSIGPENDING": "3902",
            "LimitSTACK": "18446744073709551615",
            "LoadState": "loaded",
            "MainPID": "595",
            "MemoryAccounting": "no",
            "MemoryLimit": "18446744073709551615",
            "MountFlags": "0",
            "Names": "crond.service",
            "NeedDaemonReload": "no",
            "Nice": "0",
            "NoNewPrivileges": "no",
            "NonBlocking": "no",
            "NotifyAccess": "none",
            "OOMScoreAdjust": "0",
            "OnFailureIsolate": "no",
            "PermissionsStartOnly": "no",
            "PrivateNetwork": "no",
            "PrivateTmp": "no",
            "RefuseManualStart": "no",
            "RefuseManualStop": "no",
            "RemainAfterExit": "no",
            "Requires": "basic.target",
            "Restart": "no",
            "RestartUSec": "100ms",
            "Result": "success",
            "RootDirectoryStartOnly": "no",
            "SameProcessGroup": "no",
            "SecureBits": "0",
            "SendSIGHUP": "no",
            "SendSIGKILL": "yes",
            "Slice": "system.slice",
            "StandardError": "inherit",
            "StandardInput": "null",
            "StandardOutput": "journal",
            "StartLimitAction": "none",
            "StartLimitBurst": "5",
            "StartLimitInterval": "10000000",
            "StatusErrno": "0",
            "StopWhenUnneeded": "no",
            "SubState": "running",
            "SyslogLevelPrefix": "yes",
            "SyslogPriority": "30",
            "TTYReset": "no",
            "TTYVHangup": "no",
            "TTYVTDisallocate": "no",
            "TimeoutStartUSec": "1min 30s",
            "TimeoutStopUSec": "1min 30s",
            "TimerSlackNSec": "50000",
            "Transient": "no",
            "Type": "simple",
            "UMask": "0022",
            "UnitFileState": "enabled",
            "WantedBy": "multi-user.target",
            "Wants": "system.slice",
            "WatchdogTimestampMonotonic": "0",
            "WatchdogUSec": "0",
        }
'''  # NOQA

import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.facts.system.chroot import is_chroot
from ansible.module_utils.service import sysv_exists, sysv_is_enabled, fail_if_missing
from ansible.module_utils._text import to_native


def is_running_service(service_status):
    return service_status['ActiveState'] in set(['active', 'activating', 'deactivating'])


def request_was_ignored(out):
    return '=' not in out and 'ignoring request' in out


def parse_systemctl_show(lines):
    # The output of 'systemctl show' can contain values that span multiple lines. At first glance it
    # appears that such values are always surrounded by {}, so the previous version of this code
    # assumed that any value starting with { was a multi-line value; it would then consume lines
    # until it saw a line that ended with }. However, it is possible to have a single-line value
    # that starts with { but does not end with } (this could happen in the value for Description=,
    # for example), and the previous version of this code would then consume all remaining lines as
    # part of that value. Cryptically, this would lead to Ansible reporting that the service file
    # couldn't be found.
    #
    # To avoid this issue, the following code only accepts multi-line values for keys whose names
    # start with Exec (e.g., ExecStart=), since these are the only keys whose values are known to
    # span multiple lines.
    parsed = {}
    multival = []
    k = None
    for line in lines:
        if k is None:
            if '=' in line:
                k, v = line.split('=', 1)
                if k.startswith('Exec') and v.lstrip().startswith('{'):
                    if not v.rstrip().endswith('}'):
                        multival.append(v)
                        continue
                parsed[k] = v.strip()
                k = None
        else:
            multival.append(line)
            if line.rstrip().endswith('}'):
                parsed[k] = '\n'.join(multival).strip()
                multival = []
                k = None
    return parsed


# ===========================================
# Main control flow

def main():
    # initialize
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', aliases=['service', 'unit']),
            state=dict(type='str', choices=['reloaded', 'restarted', 'started', 'stopped']),
            enabled=dict(type='bool'),
            force=dict(type='bool'),
            masked=dict(type='bool'),
            daemon_reload=dict(type='bool', default=False, aliases=['daemon-reload']),
            daemon_reexec=dict(type='bool', default=False, aliases=['daemon-reexec']),
            user=dict(type='bool'),
            scope=dict(type='str', choices=['system', 'user', 'global']),
            no_block=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
        required_one_of=[['state', 'enabled', 'masked', 'daemon_reload', 'daemon_reexec']],
        required_by=dict(
            state=('name', ),
            enabled=('name', ),
            masked=('name', ),
        ),
        mutually_exclusive=[['scope', 'user']],
    )

    unit = module.params['name']
    if unit is not None:
        for globpattern in (r"*", r"?", r"["):
            if globpattern in unit:
                module.fail_json(msg="This module does not currently support using glob patterns, found '%s' in service name: %s" % (globpattern, unit))

    # Set CLI options depending on params
    if module.params['user'] is not None:
        # handle user deprecation, mutually exclusive with scope
        module.deprecate("The 'user' option is being replaced by 'scope'", version='2.11')
        if module.params['user']:
            module.params['scope'] = 'user'
        else:
            module.params['scope'] = 'system'

    if os.getenv('XDG_RUNTIME_DIR') is None:
        os.environ['XDG_RUNTIME_DIR'] = '/run/user/%s' % (os.geteuid())

    systemctl = module.get_bin_path('systemctl', True)

    if module.params['scope'] in ('user', 'global'):
        systemctl += " --%s" % module.params['scope']

    rc = 0
    out = err = ''
    result = dict(
        name=unit,
        changed=False,
        status=dict(),
    )

    # Run daemon-reload first, if requested
    if module.params['daemon_reload'] and not module.check_mode:
        (rc, out, err) = module.run_command("%s daemon-reload" % (systemctl))
        if rc != 0:
            module.fail_json(msg='failure %d during daemon-reload: %s' % (rc, err))

    # Run daemon-reexec
    if module.params['daemon_reexec'] and not module.check_mode:
        (rc, out, err) = module.run_command("%s daemon-reexec" % (systemctl))
        if rc != 0:
            module.fail_json(msg='failure %d during daemon-reexec: %s' % (rc, err))

    if not unit:
        module.exit_json(**result)

    is_initd = sysv_exists(unit)
    is_found = False
    is_masked = False
    is_generated = True
    is_service = unit.endswith('.service')
    is_initd_generated_service = False

    # check service data, cannot error out on rc as it changes across versions
    (rc, out, err) = module.run_command("%s show '%s'" % (systemctl, unit))

    if rc == 0 and (not out or request_was_ignored(out + err)):
        # `systemctl show` can return 'Running in chroot, ignoring request.' with rc==0
        # we considere it a failure so we overwrite rc
        # we also considere it a failure if it returns nothing (I don't know if it's possible)
        rc = 1

    if rc == 0:
        # load return of systemctl show into dictionary for easy access and return
        result['status'] = parse_systemctl_show(to_native(out).split('\n'))

        is_found = result['status'].get('LoadState', 'not-found') != 'not-found'
        is_masked = result['status'].get('LoadState', 'not-found') == 'masked'
        # UnitFileState is not available on old systemd version (pre 230,
        # systemd commit f413930863ab3b98cb7bf9e761081b4e88a5d7d9)
        is_generated = result['status'].get('UnitFileState', 'generated') == 'generated'
        is_service = result['status'].get('Id', '').endswith('.service')

        # Check for loading error
        if is_found and not is_masked and 'LoadError' in result['status']:
            module.fail_json(msg="Error loading unit file '%s': %s" % (unit, result['status']['LoadError']))
    else:
        # fallback to `list-unit-files` command as `show` does not work on some systems (eg. chroot, or
        # when scope=user or global is used but systemd user instance isn't started)
        # we don't use `list-unit-files` as primary command as it requires .service (or other unit type) notation
        # and it doesn't work for generated service on old systemd version (pre 230)
        (rc, out, err) = module.run_command("%s list-unit-files '%s'" % (systemctl, unit))

        if rc == 0:
            is_found = '1 unit files listed.' in out
        else:
            # stop here, `systemctl list-unit-files` should never fail (even if it doesn't found the unit it should
            # exit with rc=0)
            module.fail_json(msg="Error `%s list-unit-files '%s'` failed" % (systemctl, unit))

        if is_found:
            is_masked = '%s masked' % (unit) in out
            is_generated = '%s generated' % (unit) in out
            # no need to overwrite `is_service` as `unit` must have the .service notation for `list-unit-files`
            # to work, so `is_service` was already good when we set it's default value (based on `unit`)

    if is_found and \
            is_generated and \
            module.params['scope'] in (None, 'system') and \
            is_initd and \
            is_service:
        is_initd_generated_service = True
        module.warn('The service (%s) is actually an init script but the system is managed by systemd' % unit)

    # mask/unmask the service, if requested ; can operate on services before they are installed
    #   some versions of systemd CAN mask/unmask non existing services (so we don't care about 'is_found')
    if module.params['masked'] is not None and module.params['masked'] != is_masked:
        result['changed'] = True

        if module.params['masked']:
            action = 'mask'
        else:
            action = 'unmask'

        if not module.check_mode:
            (rc, out, err) = module.run_command("%s %s '%s'" % (systemctl, action, unit))

            if rc != 0:
                # some versions of systemd CAN mask/unmask unknown services (is_found = False), so we only
                # report the service is unknown if `systemctl mask` fails
                fail_if_missing(module, is_found, unit, msg='host')

    # Enable/disable service startup at boot if requested
    if module.params['enabled'] is not None:
        # fail if the unit isn't known by systemd
        fail_if_missing(module, is_found, unit, msg='host')

        # do we need to enable/disable the service?
        (rc, out, err) = module.run_command("%s is-enabled '%s'" % (systemctl, unit))

        # on old systemd version (pre 230), generated (initd) service can be enabled without `systemctl is-enabled …` reporting it.
        # so rc != 0 have a special treatment
        if rc == 0 or (is_initd_generated_service and
                       not out.strip().endswith('disabled') and
                       sysv_is_enabled(unit)):
            is_enabled = True
        else:
            is_enabled = False

        # by default, record the CURRENT enabled/disabled status in module result
        result['enabled'] = is_enabled

        # Change enable/disable if needed
        if module.params['enabled'] != is_enabled:
            result['changed'] = True

            if module.params['enabled']:
                action = 'enable'
            else:
                action = 'disable'

            if module.params['force']:
                action = '--force %s' % (action)

            if not module.check_mode:
                (rc, out, err) = module.run_command("%s %s '%s'" % (systemctl, action, unit))

                if rc != 0:
                    module.fail_json(msg="Unable to %s unit %s: %s" % (action, unit, out + err))

            # update the enabled/disabled status in module result
            result['enabled'] = not is_enabled

    # set service state if requested
    if module.params['state'] is not None:
        # fail if the unit isn't known by systemd
        fail_if_missing(module, is_found, unit, msg='host')

        # by default, record the DESIRED start/stop status in module result
        result['state'] = module.params['state']

        # What is current service state?
        if 'ActiveState' in result['status']:
            action = None
            if module.params['state'] == 'started':
                if not is_running_service(result['status']):
                    action = 'start'
            elif module.params['state'] == 'stopped':
                if is_running_service(result['status']):
                    action = 'stop'
            else:  # module.params['state'] in {'restarted', 'reloaded'}
                if not is_running_service(result['status']):
                    action = 'start'
                else:
                    action = module.params['state'][:-2]  # remove 'ed' from restarted/reloaded
                result['state'] = 'started'

            if action:
                result['changed'] = True

                if module.params['no_block']:
                    action = "--no-block %s" % (action)

                if not module.check_mode:
                    (rc, out, err) = module.run_command("%s %s '%s'" % (systemctl, action, unit))
                    if rc != 0:
                        module.fail_json(msg="Unable to %s unit %s: %s" % (action, unit, err))
        # check for chroot
        elif is_chroot(module):
            module.warn("Target is a chroot. This can lead to false positives or prevent the init system tools from working.")
        else:
            # this should not happen?
            module.fail_json(msg="Unit is in unknown state", status=result['status'])

    module.exit_json(**result)


if __name__ == '__main__':
    main()
