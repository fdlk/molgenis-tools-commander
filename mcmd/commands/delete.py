import mcmd.config.config as config
from mcmd import io
from mcmd.client.molgenis_client import login, delete, delete_data, resource_exists, ResourceType
from mcmd.io import highlight
from mcmd.utils import McmdError


# =========
# Arguments
# =========

def arguments(subparsers):
    p_delete = subparsers.add_parser('delete',
                                     help='Delete entities or data',
                                     description="Run 'mcmd delete entity -h' or 'mcmd delete data -h' to view the help"
                                                 " for those sub-commands")
    p_delete_subparsers = p_delete.add_subparsers(dest="type")
    p_delete_entity = p_delete_subparsers.add_parser('entity',
                                                     help='Delete an entity(type)')
    p_delete_entity.add_argument('entity_type',
                                 type=str,
                                 help="The name of the entity you want to delete")
    p_delete_entity.add_argument('--force', '-f',
                                 action='store_true',
                                 help="Does your delete action without asking if you know it for sure")
    p_delete_entity.set_defaults(func=delete_entity,
                                 write_to_history=True)
    p_delete_data = p_delete_subparsers.add_parser('data',
                                                   help='Delete data from an entity(type)')
    p_delete_data.add_argument('entity_type',
                               type=str,
                               help="The name of the entity you want to delete all data from")
    p_delete_data.add_argument('--force', '-f',
                               action='store_true',
                               help="Does your delete action without asking if you know it for sure")
    p_delete_data.set_defaults(func=delete_all_data,
                               write_to_history=True)


# =======
# Methods
# =======

"""
Deletes an entityType or data from an entityType.
"""


def _delete_row(entity, row, msg):
    io.start(msg)
    url = '{}{}'.format(config.api('rest2'), entity)
    delete_data(url, [row])


def _delete_all_data(entity):
    io.start('Deleting all data from entity: {}'.format(entity))
    url = '{}{}'.format(config.api('rest1'), entity)
    delete(url)


def _delete_entity_type(entity):
    io.start('Deleting entity: {}'.format(highlight(entity)))
    _delete_row('sys_md_EntityType', entity, 'Deleting: {}'.format(highlight(entity)))


@login
def delete_all_data(args):
    if not resource_exists(args.entity_type, ResourceType.ENTITY_TYPE):
        raise McmdError("Entity type {} doesn't exist".format(args.entity_type))
    if args.force or (not args.force and io.confirm(
            'Are you sure you want to remove all data from entity: {}?'.format(args.entity_type))):
        _delete_all_data(args.entity_type)


@login
def delete_entity(args):
    if not resource_exists(args.entity_type, ResourceType.ENTITY_TYPE):
        raise McmdError("Entity type {} doesn't exist".format(args.entity_type))
    if args.force or (not args.force and io.confirm(
            'Are you sure you want to remove the complete entity: {}?'.format(args.entity_type))):
        _delete_entity_type(args.entity_type)
