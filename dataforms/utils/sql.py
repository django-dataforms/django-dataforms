from collections import defaultdict
from django.db import connections, models, transaction
from itertools import groupby

def query_to_grouped_dict(cursor, groupid='id'):
    """
    Converts a cursor query into a list of dictionaries, 
    grouped together on a key, usually the primary key.
    This is used primarily when doing left joins to group rows together.

    
    :arg cursor: a a cursor object 'ie - cursor.execute('select *....')
    :arg group_key: a int representing the element in the list 'keys' that to group on
    :return: a list of dictionaries with keys based on the DB's column names
        which are grouped where dicts are the same but their values may not be.
    """
    
    desc = cursor.description
    cursor_list = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
    compare_list = []
    
    results = []
    compare_list.extend(cursor_list)
    
    for index, group in groupby(cursor_list, lambda x: x[groupid]):
        
        result_dict = {}
        
        for dic in group:
            if not result_dict:
                result_dict.update(dic)
            else:
                for key, value in dic.iteritems():
                    if value != result_dict[key]:
                        if isinstance(result_dict[key], list):
                            if value not in result_dict[key]:
                                result_dict[key].append(value)
                        else:
                            result_dict[key] = [result_dict[key], value]
    
        results.append(result_dict)

    return results

def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [dict(zip([col[0] for col in desc], row))   for row in cursor.fetchall()]


def insert_many(objects, using="default"):
    """Insert list of Django objects in one SQL query. Objects must be
    of the same Django model. Note that save is not called and signals
    on the model are not raised."""
    if not objects:
        return

    con = connections[using]
    
    model = objects[0].__class__
    fields = [f for f in model._meta.fields if not isinstance(f, models.AutoField)]
    parameters = []
    for o in objects:
        parameters.append(tuple(f.get_db_prep_save(f.pre_save(o, True), connection=con) for f in fields))

    table = model._meta.db_table
    column_names = ",".join(con.ops.quote_name(f.column) for f in fields)
    placeholders = ",".join(("%s",) * len(fields))
    con.cursor().executemany(
        "insert into %s (%s) values (%s)" % (table, column_names, placeholders),
        parameters)
    transaction.commit_unless_managed()


def update_many(objects, fields=[], using="default"):
    """Update list of Django objects in one SQL query, optionally only
    overwrite the given fields (as names, e.g. fields=["foo"]).
    Objects must be of the same Django model. Note that save is not
    called and signals on the model are not raised."""
    if not objects:
        return

    con = connections[using]

    names = fields
    meta = objects[0]._meta
    fields = [f for f in meta.fields if not isinstance(f, models.AutoField) and (not names or f.name in names)]

    if not fields:
        raise ValueError("No fields to update, field names are %s." % names)
    
    fields_with_pk = fields + [meta.pk]
    parameters = []
    for o in objects:
        parameters.append(tuple(f.get_db_prep_save(f.pre_save(o, True), connection=con) for f in fields_with_pk))

    table = meta.db_table
    assignments = ",".join(("%s=%%s" % con.ops.quote_name(f.column)) for f in fields)
    con.cursor().executemany(
        "update %s set %s where %s=%%s" % (table, assignments, con.ops.quote_name(meta.pk.column)),
        parameters)
    transaction.commit_unless_managed()
    
    
def delete_many(objects, table=None, using="default"):
    
    con = connections[using]
    
    fields = [(o.id,) for o in objects]   
    meta = objects[0]._meta
    
    parameters = fields
    
    table = table or meta.db_table
    con.cursor().executemany(
        "delete from %s where %s=%%s" % (table, con.ops.quote_name(meta.pk.column)),
        parameters)
    transaction.commit_unless_managed()
    
    