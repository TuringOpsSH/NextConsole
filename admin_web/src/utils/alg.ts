import generateSchema from 'json-schema-generator';

export function generateNcSchema(obj: object) {
  // 从一个json对象中提取出nc的schema
  // 只支持string, number, boolean, object, array
  // 主要修改: ncOrders、typeName、ref
  if (!obj || typeof obj !== 'object') {
    return {};
  }
  const schema = generateSchema(obj);
  delete schema['$schema'];

  // 遍历所有type，并新增typeName字段
  traverseTypes(schema);
  // 遍历所有object，根据obj，填充value字段
  fillRef(schema, obj);
  return schema;
}
function traverseTypes(node: any) {
  // 遍历所有type，并新增typeName字段
  // 新增ncOrders字段
  node['typeName'] = node.type;
  if (node.type == 'object' && node.properties) {
    node['ncOrders'] = [];
    for (const key in node.properties) {
      node['ncOrders'].push(key);
      traverseTypes(node.properties[key]);
    }
  } else if (node.type == 'array' && node.items) {
    traverseTypes(node.items);
  }
}

function fillRef(node: any, obj) {
  // 遍历所有object，根据obj，填充ref字段
  if (node.type == 'object' && node.properties) {
    for (const key in node.properties) {
      if (obj && typeof obj === 'object' && key in obj) {
        fillRef(node.properties[key], obj[key]);
      } else {
        fillRef(node.properties[key], undefined);
      }
    }
  } else if (node.type == 'array' && node.items) {
    if (Array.isArray(obj) && obj.length > 0) {
      fillRef(node.items, obj[0]);
    } else {
      fillRef(node.items, undefined);
    }
  } else {
    // 基础类型，直接赋值
    if (obj === undefined) {
      node['ref'] = '';
      node['value'] = '';
    } else {
      node['ref'] = obj;
      node['value'] = obj;
    }
  }
}
