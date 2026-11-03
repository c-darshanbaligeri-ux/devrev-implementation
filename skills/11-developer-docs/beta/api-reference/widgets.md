# Widgets

Source: <https://developer.devrev.ai/beta/api-reference/widgets>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/widgets.create` | [create](#create) |
| GET | `/widgets.get` | [get](#get) |
| POST | `/widgets.get` | [get-post](#get-post) |

<a id="create"></a>

## `POST /widgets.create`

**Create Widget**

Source: <https://developer.devrev.ai/beta/api-reference/widgets/create>

Creates a new widget.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `apps` | no | `array<string>` | The app fragment names installed by the widget. |
| `data_sources` | no | `array<create-widget-data-source>` | Data sources provide the backing data tables for the widget. |
| `description` | no | `string` | A brief summary of what the widget displays or represents.<br>*Format: text* |
| `identifier` | no | `string` | The identifier for the widget.<br>*Value in: "agent_generated" \| "space_enhancement_default" \| "space_issue_default"* |
| `insights` | no | `string` | The insights associated with the widget for agent generated widgets.<br>*Format: text* |
| `is_draft` | no | `boolean` | Whether the widget is a draft widget. |
| `is_system` | no | `boolean` | Whether the widget is a system widget. |
| `layout` | yes | `array<create-grid-layout>` | Layout of the widget. It determines the organization of the sub widgets. |
| `name` | no | `string` | A unique identifying name for the widget (optional).<br>*Format: text* |
| `parent_id` | no | `string` | The ID of the parent surface on which this widget is embedded. Widget can be optionally part of a parent surface which can be moved to another surface.<br>*Format: id* |
| `shared_with` | no | `array<set-shared-with-membership>` | The list of users, groups and audiences with whom the widget is shared and the corresponding roles. |
| `space` | no | `string` | The space associated with the object.<br>*Format: id* |
| `sub_widgets` | yes | `array<create-sub-widget>` | A list of sub-widgets that the widget contains. Each widget can contain multiple sub-widgets. |
| `table_manifest` | no | `create-widget-table-manifest` |  |
| `title` | yes | `string` | The title of the widget.<br>*Format: text* |
| `version` | no | `string` | The version of the widget.<br>*Value in: "v0" \| "v1" \| "v2"* |

### Response codes

- `201` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/widgets.create" \
  -H "Content-Type: application/json" \
  -d '{
    "layout": [
      {
        "reference_id": "string"
      }
    ],
    "sub_widgets": [
      {
        "reference_id": "string",
        "visualization": {
          "type": "bar"
        }
      }
    ],
    "title": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "widget": {
    "created_by": {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    },
    "created_date": "2023-01-01T12:00:00.000Z",
    "display_id": "string",
    "id": "string",
    "modified_by": {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    },
    "modified_date": "2023-01-01T12:00:00.000Z",
    "object_version": 0,
    "data_sources": [
      {
        "type": "api",
        "api": {
          "include": [
            {
              "type": "issue",
              "display_id": "string",
              "id": "string",
              "owned_by": [
                {
                  "type": "dev_user",
                  "display_id": "string",
                  "id": "string",
                  "display_name": "string",
                  "display_picture": {
                    "display_id": "string",
                    "id": "string",
                    "file": {
                      "type": "string",
                      "name": "string",
                      "size": 0
                    }
                  },
                  "email": "string",
                  "full_name": "string",
                  "state": "active"
                }
              ],
              "stage": {
                "name": "string",
                "stage": {
                  "display_id": "string",
                  "id": "string",
                  "name": "string",
                  "sync_metadata": {
                    "external_reference": "string",
                    "last_sync_in": {
                      "status": "failed",
                      "sync_unit": {
                        "display_id": "string",
                        "id": "string",
                        "external_sync_unit_name": "string",
                        "external_system_id": "string",
                        "external_system_name": "string",
                        "external_system_type": "adaas",
                        "is_archived": true,
                        "name": "string",
                        "sync_run": {
                          "mode": "initial",
                          "progress": {
                            "state": "completed"
                          },
                          "reserved_rate_limit_percentage": 0
                        },
                        "sync_type": "manual"
                      }
                    },
                    "origin_system": "string"
                  }
                }
              },
              "state_display_name": "string",
              "sync_metadata": {
                "external_reference": "string",
                "last_sync_in": {
                  "status": "failed",
                  "sync_unit": {
                    "display_id": "string",
                    "id": "string",
                    "external_sync_unit_name": "string",
                    "external_system_id": "string",
                    "external_system_name": "string",
                    "external_system_type": "adaas",
                    "is_archived": true,
                    "name": "string",
                    "sync_run": {
                      "mode": "initial",
                      "progress": {
                        "state": "completed"
                      },
                      "reserved_rate_limit_percentage": 0
                    },
                    "sync_type": "manual"
                  }
                },
                "origin_system": "string"
              },
              "title": "string",
              "display_id_alias": "string",
              "priority": "p0",
              "priority_v2": {
                "id": 0,
                "label": "string",
                "ordinal": 0
              },
              "space": "string",
              "sprint": {
                "type": "curated",
                "end_date": "2023-01-01T12:00:00.000Z",
                "id": "string",
                "name": "string",
                "start_date": "2023-01-01T12:00:00.000Z",
                "state": "active"
              }
            }
          ],
          "is_custom_leaf_type": true,
          "leaf_type": "string",
          "subtypes": [
            "string"
          ]
        },
        "data_source": "string",
        "dimensions": [
          {
            "type": "custom_field",
            "custom_field": {
              "leaf_type": "string",
              "name": "string",
              "subtype": "string"
            },
            "devrev_schema": {
              "field_type": "array",
              "description": "string",
              "is_derived": true,
              "is_filterable": true,
              "is_immutable": true,
              "is_pii": true,
              "is_required": true,
              "mfz": {},
              "name": "string",
              "oasis": {},
              "origin": "string",
              "ui": {
                "card_view": {
                  "is_visible": true
                },
                "client_overrides": [
                  {
                    "client_name": "string",
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_overrides": [
                      {
                        "decimal_places": 0,
                        "display_name": "string",
                        "is_groupable": true,
                        "is_hidden": true,
                        "is_required": true,
                        "order": 0,
                        "placeholder": "string",
                        "search_query": "string",
                        "tooltip": "string",
                        "use_shorthand_notation": true,
                        "view_name": "string"
                      }
                    ]
                  }
                ],
                "create_view": {
                  "is_hidden": true
                },
                "decimal_places": 0,
                "detail_view": {
                  "is_hidden": true
                },
                "display_name": "string",
                "filter_view": {
                  "is_hidden": true
                },
                "group_name": "string",
                "is_active_in_detail_view": true,
                "is_bulk_action_enabled": true,
                "is_currency_field": true,
                "is_groupable": true,
                "is_hidden": true,
                "is_hidden_during_create": true,
                "is_read_only": true,
                "is_required": true,
                "is_shown_in_summary": true,
                "is_sortable": true,
                "list_view": {
                  "is_hidden": true
                },
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "summary_view": {
                  "is_hidden": true
                },
                "tooltip": "string",
                "unit": "string",
                "use_shorthand_notation": true
              },
              "default_value": true
            },
            "has_custom_expression": true,
            "is_derived": true,
            "meerkat_schema": {
              "type": "boolean",
              "function": {
                "type": "avg"
              },
              "sql_expression": "string",
              "timestamp_rollup": "day"
            },
            "reference_name": "string"
          }
        ],
        "external_data_source": {
          "dataset_projections": [
            {
              "columns": [
                {
                  "custom_field": {
                    "leaf_type": "string",
                    "name": "string",
                    "subtype": "string"
                  },
                  "name": "string"
                }
              ],
              "dataset": "string"
            }
          ],
          "id": "string"
        },
        "joins": [
          {}
        ],
        "measures": [
          {
            "type": "custom_field",
            "custom_field": {
              "leaf_type": "string",
              "name": "string",
              "subtype": "string"
            },
            "devrev_schema": {
              "field_type": "array",
              "description": "string",
              "is_derived": true,
              "is_filterable": true,
              "is_immutable": true,
              "is_pii": true,
              "is_required": true,
              "mfz": {},
              "name": "string",
              "oasis": {},
              "origin": "string",
              "ui": {
                "card_view": {
                  "is_visible": true
                },
                "client_overrides": [
                  {
                    "client_name": "string",
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_overrides": [
                      {
                        "decimal_places": 0,
                        "display_name": "string",
                        "is_groupable": true,
                        "is_hidden": true,
                        "is_required": true,
                        "order": 0,
                        "placeholder": "string",
                        "search_query": "string",
                        "tooltip": "string",
                        "use_shorthand_notation": true,
                        "view_name": "string"
                      }
                    ]
                  }
                ],
                "create_view": {
                  "is_hidden": true
                },
                "decimal_places": 0,
                "detail_view": {
                  "is_hidden": true
                },
                "display_name": "string",
                "filter_view": {
                  "is_hidden": true
                },
                "group_name": "string",
                "is_active_in_detail_view": true,
                "is_bulk_action_enabled": true,
                "is_currency_field": true,
                "is_groupable": true,
                "is_hidden": true,
                "is_hidden_during_create": true,
                "is_read_only": true,
                "is_required": true,
                "is_shown_in_summary": true,
                "is_sortable": true,
                "list_view": {
                  "is_hidden": true
                },
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "summary_view": {
                  "is_hidden": true
                },
                "tooltip": "string",
                "unit": "string",
                "use_shorthand_notation": true
              },
              "default_value": true
            },
            "has_custom_expression": true,
            "is_derived": true,
            "meerkat_schema": {
              "type": "boolean",
              "function": {
                "type": "avg"
              },
              "sql_expression": "string",
              "timestamp_rollup": "day"
            },
            "reference_name": "string"
          }
        ],
        "oasis": {
          "datasets": [
            "string"
          ],
          "projections": [
            {
              "columns": [
                {
                  "custom_field": {
                    "leaf_type": "string",
                    "name": "string",
                    "subtype": "string"
                  },
                  "name": "string"
                }
              ],
              "dataset": "string"
            }
          ],
          "sql_query": "string"
        },
        "reference_name": "string"
      }
    ],
    "description": "string",
    "insights": "string",
    "is_draft": true,
    "is_system": true,
    "layout": [
      {
        "layout": [
          {
            "layout": [],
            "position": {
              "height": 0,
              "width": 0,
              "x": 0,
              "y": 0
            },
            "reference_id": "string"
          }
        ],
        "position": {
          "height": 0,
          "width": 0,
          "x": 0,
          "y": 0
        },
        "reference_id": "string"
      }
    ],
    "name": "string",
    "sub_widgets": [
      {
        "pinned_filters": [
          {
            "reference_name": "string"
          }
        ],
        "query": {
          "dimension_configs": [
            {
              "type": "aggregation",
              "aggregation": "avg",
              "column_name": "string",
              "reference_name": "string",
              "time_granularity": "day"
            }
          ],
          "dimensions": [
            "string"
          ],
          "filters": [
            {}
          ],
          "joins": [
            {
              "path": [
                "string"
              ]
            }
          ],
          "limit": 0,
          "measure_configs": [
            {
              "type": "aggregation",
              "aggregation": "avg",
              "column_name": "string",
              "reference_name": "string",
              "time_granularity": "day"
            }
          ],
          "measures": [
            "string"
          ],
          "order_by": [
            {
              "direction": "ascending",
              "reference_name": "string"
            }
          ]
        },
        "reference_id": "string",
        "visualization": {
          "type": "bar",
          "bar": {
            "data_labels": {
              "display_mode": "percentage",
              "enable": true
            },
            "is_stacked": true,
            "scrollbar": {},
            "show_data_labels": true,
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "column": {
            "data_labels": {
              "display_mode": "percentage",
              "enable": true
            },
            "is_stacked": true,
            "scrollbar": {},
            "show_data_labels": true,
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "donut": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            }
          },
          "flame_graph": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "heatmap": {
            "color": "string",
            "x": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            },
            "y": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            },
            "z": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            }
          },
          "kanban": {
            "card_attributes": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "order": 0,
                "position": "body",
                "reference_name": "string"
              }
            ],
            "group_by": [
              {
                "key": "string",
                "limit": 0
              }
            ]
          },
          "line": {
            "is_stacked": true,
            "show_data_labels": true,
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_area_filled": true,
                "is_hidden": true,
                "is_spline": true,
                "label": "string",
                "marker": true,
                "reference_name": "string"
              }
            ]
          },
          "metric": {
            "pvp": {
              "enabled": true,
              "invert_correlation_color": true
            },
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "packed_bubble": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "pie": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            }
          },
          "rich_text": {
            "content": {}
          },
          "scatter": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "table": {
            "columns": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "is_movable": true,
                "is_pinned": true,
                "is_resizable": true,
                "is_sortable": true,
                "is_visibility_togglable": true,
                "label": "string",
                "lock_position": "left",
                "max_width": 0,
                "min_width": 0,
                "order": 0,
                "pin_position": "left",
                "reference_name": "string",
                "width": 0
              }
            ],
            "group_by": [
              {
                "key": "string",
                "limit": 0
              }
            ]
          }
        }
      }
    ],
    "table_manifest": {},
    "title": "string"
  }
}
```

</details>


<a id="get"></a>

## `GET /widgets.get`

**Get Widget**

Source: <https://developer.devrev.ai/beta/api-reference/widgets/get>

Returns the requested widget.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The requested widget's ID.<br>*Format: id* |

### Response codes

- `200` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X GET "https://api.devrev.ai/widgets.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "widget": {
    "created_by": {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    },
    "created_date": "2023-01-01T12:00:00.000Z",
    "display_id": "string",
    "id": "string",
    "modified_by": {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    },
    "modified_date": "2023-01-01T12:00:00.000Z",
    "object_version": 0,
    "data_sources": [
      {
        "type": "api",
        "api": {
          "include": [
            {
              "type": "issue",
              "display_id": "string",
              "id": "string",
              "owned_by": [
                {
                  "type": "dev_user",
                  "display_id": "string",
                  "id": "string",
                  "display_name": "string",
                  "display_picture": {
                    "display_id": "string",
                    "id": "string",
                    "file": {
                      "type": "string",
                      "name": "string",
                      "size": 0
                    }
                  },
                  "email": "string",
                  "full_name": "string",
                  "state": "active"
                }
              ],
              "stage": {
                "name": "string",
                "stage": {
                  "display_id": "string",
                  "id": "string",
                  "name": "string",
                  "sync_metadata": {
                    "external_reference": "string",
                    "last_sync_in": {
                      "status": "failed",
                      "sync_unit": {
                        "display_id": "string",
                        "id": "string",
                        "external_sync_unit_name": "string",
                        "external_system_id": "string",
                        "external_system_name": "string",
                        "external_system_type": "adaas",
                        "is_archived": true,
                        "name": "string",
                        "sync_run": {
                          "mode": "initial",
                          "progress": {
                            "state": "completed"
                          },
                          "reserved_rate_limit_percentage": 0
                        },
                        "sync_type": "manual"
                      }
                    },
                    "origin_system": "string"
                  }
                }
              },
              "state_display_name": "string",
              "sync_metadata": {
                "external_reference": "string",
                "last_sync_in": {
                  "status": "failed",
                  "sync_unit": {
                    "display_id": "string",
                    "id": "string",
                    "external_sync_unit_name": "string",
                    "external_system_id": "string",
                    "external_system_name": "string",
                    "external_system_type": "adaas",
                    "is_archived": true,
                    "name": "string",
                    "sync_run": {
                      "mode": "initial",
                      "progress": {
                        "state": "completed"
                      },
                      "reserved_rate_limit_percentage": 0
                    },
                    "sync_type": "manual"
                  }
                },
                "origin_system": "string"
              },
              "title": "string",
              "display_id_alias": "string",
              "priority": "p0",
              "priority_v2": {
                "id": 0,
                "label": "string",
                "ordinal": 0
              },
              "space": "string",
              "sprint": {
                "type": "curated",
                "end_date": "2023-01-01T12:00:00.000Z",
                "id": "string",
                "name": "string",
                "start_date": "2023-01-01T12:00:00.000Z",
                "state": "active"
              }
            }
          ],
          "is_custom_leaf_type": true,
          "leaf_type": "string",
          "subtypes": [
            "string"
          ]
        },
        "data_source": "string",
        "dimensions": [
          {
            "type": "custom_field",
            "custom_field": {
              "leaf_type": "string",
              "name": "string",
              "subtype": "string"
            },
            "devrev_schema": {
              "field_type": "array",
              "description": "string",
              "is_derived": true,
              "is_filterable": true,
              "is_immutable": true,
              "is_pii": true,
              "is_required": true,
              "mfz": {},
              "name": "string",
              "oasis": {},
              "origin": "string",
              "ui": {
                "card_view": {
                  "is_visible": true
                },
                "client_overrides": [
                  {
                    "client_name": "string",
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_overrides": [
                      {
                        "decimal_places": 0,
                        "display_name": "string",
                        "is_groupable": true,
                        "is_hidden": true,
                        "is_required": true,
                        "order": 0,
                        "placeholder": "string",
                        "search_query": "string",
                        "tooltip": "string",
                        "use_shorthand_notation": true,
                        "view_name": "string"
                      }
                    ]
                  }
                ],
                "create_view": {
                  "is_hidden": true
                },
                "decimal_places": 0,
                "detail_view": {
                  "is_hidden": true
                },
                "display_name": "string",
                "filter_view": {
                  "is_hidden": true
                },
                "group_name": "string",
                "is_active_in_detail_view": true,
                "is_bulk_action_enabled": true,
                "is_currency_field": true,
                "is_groupable": true,
                "is_hidden": true,
                "is_hidden_during_create": true,
                "is_read_only": true,
                "is_required": true,
                "is_shown_in_summary": true,
                "is_sortable": true,
                "list_view": {
                  "is_hidden": true
                },
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "summary_view": {
                  "is_hidden": true
                },
                "tooltip": "string",
                "unit": "string",
                "use_shorthand_notation": true
              },
              "default_value": true
            },
            "has_custom_expression": true,
            "is_derived": true,
            "meerkat_schema": {
              "type": "boolean",
              "function": {
                "type": "avg"
              },
              "sql_expression": "string",
              "timestamp_rollup": "day"
            },
            "reference_name": "string"
          }
        ],
        "external_data_source": {
          "dataset_projections": [
            {
              "columns": [
                {
                  "custom_field": {
                    "leaf_type": "string",
                    "name": "string",
                    "subtype": "string"
                  },
                  "name": "string"
                }
              ],
              "dataset": "string"
            }
          ],
          "id": "string"
        },
        "joins": [
          {}
        ],
        "measures": [
          {
            "type": "custom_field",
            "custom_field": {
              "leaf_type": "string",
              "name": "string",
              "subtype": "string"
            },
            "devrev_schema": {
              "field_type": "array",
              "description": "string",
              "is_derived": true,
              "is_filterable": true,
              "is_immutable": true,
              "is_pii": true,
              "is_required": true,
              "mfz": {},
              "name": "string",
              "oasis": {},
              "origin": "string",
              "ui": {
                "card_view": {
                  "is_visible": true
                },
                "client_overrides": [
                  {
                    "client_name": "string",
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_overrides": [
                      {
                        "decimal_places": 0,
                        "display_name": "string",
                        "is_groupable": true,
                        "is_hidden": true,
                        "is_required": true,
                        "order": 0,
                        "placeholder": "string",
                        "search_query": "string",
                        "tooltip": "string",
                        "use_shorthand_notation": true,
                        "view_name": "string"
                      }
                    ]
                  }
                ],
                "create_view": {
                  "is_hidden": true
                },
                "decimal_places": 0,
                "detail_view": {
                  "is_hidden": true
                },
                "display_name": "string",
                "filter_view": {
                  "is_hidden": true
                },
                "group_name": "string",
                "is_active_in_detail_view": true,
                "is_bulk_action_enabled": true,
                "is_currency_field": true,
                "is_groupable": true,
                "is_hidden": true,
                "is_hidden_during_create": true,
                "is_read_only": true,
                "is_required": true,
                "is_shown_in_summary": true,
                "is_sortable": true,
                "list_view": {
                  "is_hidden": true
                },
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "summary_view": {
                  "is_hidden": true
                },
                "tooltip": "string",
                "unit": "string",
                "use_shorthand_notation": true
              },
              "default_value": true
            },
            "has_custom_expression": true,
            "is_derived": true,
            "meerkat_schema": {
              "type": "boolean",
              "function": {
                "type": "avg"
              },
              "sql_expression": "string",
              "timestamp_rollup": "day"
            },
            "reference_name": "string"
          }
        ],
        "oasis": {
          "datasets": [
            "string"
          ],
          "projections": [
            {
              "columns": [
                {
                  "custom_field": {
                    "leaf_type": "string",
                    "name": "string",
                    "subtype": "string"
                  },
                  "name": "string"
                }
              ],
              "dataset": "string"
            }
          ],
          "sql_query": "string"
        },
        "reference_name": "string"
      }
    ],
    "description": "string",
    "insights": "string",
    "is_draft": true,
    "is_system": true,
    "layout": [
      {
        "layout": [
          {
            "layout": [],
            "position": {
              "height": 0,
              "width": 0,
              "x": 0,
              "y": 0
            },
            "reference_id": "string"
          }
        ],
        "position": {
          "height": 0,
          "width": 0,
          "x": 0,
          "y": 0
        },
        "reference_id": "string"
      }
    ],
    "name": "string",
    "sub_widgets": [
      {
        "pinned_filters": [
          {
            "reference_name": "string"
          }
        ],
        "query": {
          "dimension_configs": [
            {
              "type": "aggregation",
              "aggregation": "avg",
              "column_name": "string",
              "reference_name": "string",
              "time_granularity": "day"
            }
          ],
          "dimensions": [
            "string"
          ],
          "filters": [
            {}
          ],
          "joins": [
            {
              "path": [
                "string"
              ]
            }
          ],
          "limit": 0,
          "measure_configs": [
            {
              "type": "aggregation",
              "aggregation": "avg",
              "column_name": "string",
              "reference_name": "string",
              "time_granularity": "day"
            }
          ],
          "measures": [
            "string"
          ],
          "order_by": [
            {
              "direction": "ascending",
              "reference_name": "string"
            }
          ]
        },
        "reference_id": "string",
        "visualization": {
          "type": "bar",
          "bar": {
            "data_labels": {
              "display_mode": "percentage",
              "enable": true
            },
            "is_stacked": true,
            "scrollbar": {},
            "show_data_labels": true,
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "column": {
            "data_labels": {
              "display_mode": "percentage",
              "enable": true
            },
            "is_stacked": true,
            "scrollbar": {},
            "show_data_labels": true,
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "donut": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            }
          },
          "flame_graph": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "heatmap": {
            "color": "string",
            "x": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            },
            "y": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            },
            "z": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            }
          },
          "kanban": {
            "card_attributes": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "order": 0,
                "position": "body",
                "reference_name": "string"
              }
            ],
            "group_by": [
              {
                "key": "string",
                "limit": 0
              }
            ]
          },
          "line": {
            "is_stacked": true,
            "show_data_labels": true,
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_area_filled": true,
                "is_hidden": true,
                "is_spline": true,
                "label": "string",
                "marker": true,
                "reference_name": "string"
              }
            ]
          },
          "metric": {
            "pvp": {
              "enabled": true,
              "invert_correlation_color": true
            },
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "packed_bubble": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "pie": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            }
          },
          "rich_text": {
            "content": {}
          },
          "scatter": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "table": {
            "columns": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "is_movable": true,
                "is_pinned": true,
                "is_resizable": true,
                "is_sortable": true,
                "is_visibility_togglable": true,
                "label": "string",
                "lock_position": "left",
                "max_width": 0,
                "min_width": 0,
                "order": 0,
                "pin_position": "left",
                "reference_name": "string",
                "width": 0
              }
            ],
            "group_by": [
              {
                "key": "string",
                "limit": 0
              }
            ]
          }
        }
      }
    ],
    "table_manifest": {},
    "title": "string"
  }
}
```

</details>


<a id="get-post"></a>

## `POST /widgets.get`

**Get Widget (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/widgets/get-post>

Returns the requested widget.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The requested widget's ID.<br>*Format: id* |

### Response codes

- `200` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/widgets.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "widget": {
    "created_by": {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    },
    "created_date": "2023-01-01T12:00:00.000Z",
    "display_id": "string",
    "id": "string",
    "modified_by": {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    },
    "modified_date": "2023-01-01T12:00:00.000Z",
    "object_version": 0,
    "data_sources": [
      {
        "type": "api",
        "api": {
          "include": [
            {
              "type": "issue",
              "display_id": "string",
              "id": "string",
              "owned_by": [
                {
                  "type": "dev_user",
                  "display_id": "string",
                  "id": "string",
                  "display_name": "string",
                  "display_picture": {
                    "display_id": "string",
                    "id": "string",
                    "file": {
                      "type": "string",
                      "name": "string",
                      "size": 0
                    }
                  },
                  "email": "string",
                  "full_name": "string",
                  "state": "active"
                }
              ],
              "stage": {
                "name": "string",
                "stage": {
                  "display_id": "string",
                  "id": "string",
                  "name": "string",
                  "sync_metadata": {
                    "external_reference": "string",
                    "last_sync_in": {
                      "status": "failed",
                      "sync_unit": {
                        "display_id": "string",
                        "id": "string",
                        "external_sync_unit_name": "string",
                        "external_system_id": "string",
                        "external_system_name": "string",
                        "external_system_type": "adaas",
                        "is_archived": true,
                        "name": "string",
                        "sync_run": {
                          "mode": "initial",
                          "progress": {
                            "state": "completed"
                          },
                          "reserved_rate_limit_percentage": 0
                        },
                        "sync_type": "manual"
                      }
                    },
                    "origin_system": "string"
                  }
                }
              },
              "state_display_name": "string",
              "sync_metadata": {
                "external_reference": "string",
                "last_sync_in": {
                  "status": "failed",
                  "sync_unit": {
                    "display_id": "string",
                    "id": "string",
                    "external_sync_unit_name": "string",
                    "external_system_id": "string",
                    "external_system_name": "string",
                    "external_system_type": "adaas",
                    "is_archived": true,
                    "name": "string",
                    "sync_run": {
                      "mode": "initial",
                      "progress": {
                        "state": "completed"
                      },
                      "reserved_rate_limit_percentage": 0
                    },
                    "sync_type": "manual"
                  }
                },
                "origin_system": "string"
              },
              "title": "string",
              "display_id_alias": "string",
              "priority": "p0",
              "priority_v2": {
                "id": 0,
                "label": "string",
                "ordinal": 0
              },
              "space": "string",
              "sprint": {
                "type": "curated",
                "end_date": "2023-01-01T12:00:00.000Z",
                "id": "string",
                "name": "string",
                "start_date": "2023-01-01T12:00:00.000Z",
                "state": "active"
              }
            }
          ],
          "is_custom_leaf_type": true,
          "leaf_type": "string",
          "subtypes": [
            "string"
          ]
        },
        "data_source": "string",
        "dimensions": [
          {
            "type": "custom_field",
            "custom_field": {
              "leaf_type": "string",
              "name": "string",
              "subtype": "string"
            },
            "devrev_schema": {
              "field_type": "array",
              "description": "string",
              "is_derived": true,
              "is_filterable": true,
              "is_immutable": true,
              "is_pii": true,
              "is_required": true,
              "mfz": {},
              "name": "string",
              "oasis": {},
              "origin": "string",
              "ui": {
                "card_view": {
                  "is_visible": true
                },
                "client_overrides": [
                  {
                    "client_name": "string",
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_overrides": [
                      {
                        "decimal_places": 0,
                        "display_name": "string",
                        "is_groupable": true,
                        "is_hidden": true,
                        "is_required": true,
                        "order": 0,
                        "placeholder": "string",
                        "search_query": "string",
                        "tooltip": "string",
                        "use_shorthand_notation": true,
                        "view_name": "string"
                      }
                    ]
                  }
                ],
                "create_view": {
                  "is_hidden": true
                },
                "decimal_places": 0,
                "detail_view": {
                  "is_hidden": true
                },
                "display_name": "string",
                "filter_view": {
                  "is_hidden": true
                },
                "group_name": "string",
                "is_active_in_detail_view": true,
                "is_bulk_action_enabled": true,
                "is_currency_field": true,
                "is_groupable": true,
                "is_hidden": true,
                "is_hidden_during_create": true,
                "is_read_only": true,
                "is_required": true,
                "is_shown_in_summary": true,
                "is_sortable": true,
                "list_view": {
                  "is_hidden": true
                },
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "summary_view": {
                  "is_hidden": true
                },
                "tooltip": "string",
                "unit": "string",
                "use_shorthand_notation": true
              },
              "default_value": true
            },
            "has_custom_expression": true,
            "is_derived": true,
            "meerkat_schema": {
              "type": "boolean",
              "function": {
                "type": "avg"
              },
              "sql_expression": "string",
              "timestamp_rollup": "day"
            },
            "reference_name": "string"
          }
        ],
        "external_data_source": {
          "dataset_projections": [
            {
              "columns": [
                {
                  "custom_field": {
                    "leaf_type": "string",
                    "name": "string",
                    "subtype": "string"
                  },
                  "name": "string"
                }
              ],
              "dataset": "string"
            }
          ],
          "id": "string"
        },
        "joins": [
          {}
        ],
        "measures": [
          {
            "type": "custom_field",
            "custom_field": {
              "leaf_type": "string",
              "name": "string",
              "subtype": "string"
            },
            "devrev_schema": {
              "field_type": "array",
              "description": "string",
              "is_derived": true,
              "is_filterable": true,
              "is_immutable": true,
              "is_pii": true,
              "is_required": true,
              "mfz": {},
              "name": "string",
              "oasis": {},
              "origin": "string",
              "ui": {
                "card_view": {
                  "is_visible": true
                },
                "client_overrides": [
                  {
                    "client_name": "string",
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_overrides": [
                      {
                        "decimal_places": 0,
                        "display_name": "string",
                        "is_groupable": true,
                        "is_hidden": true,
                        "is_required": true,
                        "order": 0,
                        "placeholder": "string",
                        "search_query": "string",
                        "tooltip": "string",
                        "use_shorthand_notation": true,
                        "view_name": "string"
                      }
                    ]
                  }
                ],
                "create_view": {
                  "is_hidden": true
                },
                "decimal_places": 0,
                "detail_view": {
                  "is_hidden": true
                },
                "display_name": "string",
                "filter_view": {
                  "is_hidden": true
                },
                "group_name": "string",
                "is_active_in_detail_view": true,
                "is_bulk_action_enabled": true,
                "is_currency_field": true,
                "is_groupable": true,
                "is_hidden": true,
                "is_hidden_during_create": true,
                "is_read_only": true,
                "is_required": true,
                "is_shown_in_summary": true,
                "is_sortable": true,
                "list_view": {
                  "is_hidden": true
                },
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "summary_view": {
                  "is_hidden": true
                },
                "tooltip": "string",
                "unit": "string",
                "use_shorthand_notation": true
              },
              "default_value": true
            },
            "has_custom_expression": true,
            "is_derived": true,
            "meerkat_schema": {
              "type": "boolean",
              "function": {
                "type": "avg"
              },
              "sql_expression": "string",
              "timestamp_rollup": "day"
            },
            "reference_name": "string"
          }
        ],
        "oasis": {
          "datasets": [
            "string"
          ],
          "projections": [
            {
              "columns": [
                {
                  "custom_field": {
                    "leaf_type": "string",
                    "name": "string",
                    "subtype": "string"
                  },
                  "name": "string"
                }
              ],
              "dataset": "string"
            }
          ],
          "sql_query": "string"
        },
        "reference_name": "string"
      }
    ],
    "description": "string",
    "insights": "string",
    "is_draft": true,
    "is_system": true,
    "layout": [
      {
        "layout": [
          {
            "layout": [],
            "position": {
              "height": 0,
              "width": 0,
              "x": 0,
              "y": 0
            },
            "reference_id": "string"
          }
        ],
        "position": {
          "height": 0,
          "width": 0,
          "x": 0,
          "y": 0
        },
        "reference_id": "string"
      }
    ],
    "name": "string",
    "sub_widgets": [
      {
        "pinned_filters": [
          {
            "reference_name": "string"
          }
        ],
        "query": {
          "dimension_configs": [
            {
              "type": "aggregation",
              "aggregation": "avg",
              "column_name": "string",
              "reference_name": "string",
              "time_granularity": "day"
            }
          ],
          "dimensions": [
            "string"
          ],
          "filters": [
            {}
          ],
          "joins": [
            {
              "path": [
                "string"
              ]
            }
          ],
          "limit": 0,
          "measure_configs": [
            {
              "type": "aggregation",
              "aggregation": "avg",
              "column_name": "string",
              "reference_name": "string",
              "time_granularity": "day"
            }
          ],
          "measures": [
            "string"
          ],
          "order_by": [
            {
              "direction": "ascending",
              "reference_name": "string"
            }
          ]
        },
        "reference_id": "string",
        "visualization": {
          "type": "bar",
          "bar": {
            "data_labels": {
              "display_mode": "percentage",
              "enable": true
            },
            "is_stacked": true,
            "scrollbar": {},
            "show_data_labels": true,
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "column": {
            "data_labels": {
              "display_mode": "percentage",
              "enable": true
            },
            "is_stacked": true,
            "scrollbar": {},
            "show_data_labels": true,
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "donut": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            }
          },
          "flame_graph": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "heatmap": {
            "color": "string",
            "x": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            },
            "y": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            },
            "z": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            }
          },
          "kanban": {
            "card_attributes": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "order": 0,
                "position": "body",
                "reference_name": "string"
              }
            ],
            "group_by": [
              {
                "key": "string",
                "limit": 0
              }
            ]
          },
          "line": {
            "is_stacked": true,
            "show_data_labels": true,
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_area_filled": true,
                "is_hidden": true,
                "is_spline": true,
                "label": "string",
                "marker": true,
                "reference_name": "string"
              }
            ]
          },
          "metric": {
            "pvp": {
              "enabled": true,
              "invert_correlation_color": true
            },
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "packed_bubble": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "pie": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": {
              "color": {
                "type": "key_lookup",
                "key_lookup": [
                  {
                    "key": "string",
                    "value": "string"
                  }
                ],
                "static": "string"
              },
              "drill_throughs": [
                {}
              ],
              "is_hidden": true,
              "label": "string",
              "reference_name": "string"
            }
          },
          "rich_text": {
            "content": {}
          },
          "scatter": {
            "x": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ],
            "y": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "label": "string",
                "reference_name": "string"
              }
            ]
          },
          "table": {
            "columns": [
              {
                "color": {
                  "type": "key_lookup",
                  "key_lookup": [
                    {
                      "key": "string",
                      "value": "string"
                    }
                  ],
                  "static": "string"
                },
                "drill_throughs": [
                  {}
                ],
                "is_hidden": true,
                "is_movable": true,
                "is_pinned": true,
                "is_resizable": true,
                "is_sortable": true,
                "is_visibility_togglable": true,
                "label": "string",
                "lock_position": "left",
                "max_width": 0,
                "min_width": 0,
                "order": 0,
                "pin_position": "left",
                "reference_name": "string",
                "width": 0
              }
            ],
            "group_by": [
              {
                "key": "string",
                "limit": 0
              }
            ]
          }
        }
      }
    ],
    "table_manifest": {},
    "title": "string"
  }
}
```

</details>
