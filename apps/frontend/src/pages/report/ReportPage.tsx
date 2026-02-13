/**
 * 报表页面组件
 */
import React, { useState, useEffect } from 'react';
import {
  Card,
  Tabs,
  DatePicker,
  Button,
  Space,
  Spin,
  message,
  Row,
  Col,
  Statistic,
  Table,
  Dropdown,
} from 'antd';
import {
  DownloadOutlined,
  FileExcelOutlined,
  FilePdfOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  ShoppingCartOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';
import dayjs from 'dayjs';
import isoWeek from 'dayjs/plugin/isoWeek';
import weekOfYear from 'dayjs/plugin/weekOfYear';
import useReportStore from '@/store/reportStore';
import type { ReportData, ReportType, ExportFormat } from '@/types/report';

dayjs.extend(isoWeek);
dayjs.extend(weekOfYear);

const { RangePicker } = DatePicker;

/**
 * 报表页面组件
 */
const ReportPage: React.FC = () => {
  const [reportType, setReportType] = useState<ReportType>('daily');
  const [selectedDate, setSelectedDate] = useState<dayjs.Dayjs>(dayjs());
  const [selectedWeek, setSelectedWeek] = useState<[dayjs.Dayjs, dayjs.Dayjs]>([
    dayjs().startOf('isoWeek'),
    dayjs().endOf('isoWeek'),
  ]);
  const [selectedMonth, setSelectedMonth] = useState<dayjs.Dayjs>(dayjs());
  const [customDateRange, setCustomDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs]>([
    dayjs().subtract(7, 'day'),
    dayjs(),
  ]);

  const {
    dailyReport,
    weeklyReport,
    monthlyReport,
    customReport,
    isLoading,
    error,
    getDailyReport,
    getWeeklyReport,
    getMonthlyReport,
    getCustomReport,
    exportReport,
    clearError,
  } = useReportStore();

  useEffect(() => {
    loadReport();
  }, [reportType, selectedDate, selectedWeek, selectedMonth, customDateRange]);

  useEffect(() => {
    if (error) {
      message.error(error);
      clearError();
    }
  }, [error, clearError]);

  /**
   * 加载报表数据
   */
  const loadReport = () => {
    switch (reportType) {
      case 'daily':
        getDailyReport(selectedDate.format('YYYY-MM-DD'));
        break;
      case 'weekly':
        getWeeklyReport(
          selectedWeek[0].format('YYYY-MM-DD'),
          selectedWeek[1].format('YYYY-MM-DD')
        );
        break;
      case 'monthly':
        getMonthlyReport(selectedMonth.year(), selectedMonth.month() + 1);
        break;
      case 'custom':
        getCustomReport({
          start_date: customDateRange[0].format('YYYY-MM-DD'),
          end_date: customDateRange[1].format('YYYY-MM-DD'),
          type: 'all',
        });
        break;
    }
  };

  /**
   * 获取当前报表数据
   */
  const getCurrentReport = (): ReportData | null => {
    switch (reportType) {
      case 'daily':
        return dailyReport;
      case 'weekly':
        return weeklyReport;
      case 'monthly':
        return monthlyReport;
      case 'custom':
        return customReport;
      default:
        return null;
    }
  };

  /**
   * 处理导出报表
   */
  const handleExport = async (format: ExportFormat) => {
    const reportData = getCurrentReport();
    if (!reportData) {
      message.warning('暂无报表数据可导出');
      return;
    }

    try {
      await exportReport(reportData, format, reportType);
      message.success('报表导出成功');
    } catch (err) {
      message.error('报表导出失败');
    }
  };

  /**
   * 导出菜单项
   */
  const exportMenuItems: MenuProps['items'] = [
    {
      key: 'excel',
      icon: <FileExcelOutlined />,
      label: '导出Excel',
      onClick: () => handleExport('excel'),
    },
    {
      key: 'pdf',
      icon: <FilePdfOutlined />,
      label: '导出PDF',
      onClick: () => handleExport('pdf'),
    },
  ];

  /**
   * 渲染日期选择器
   */
  const renderDatePicker = () => {
    switch (reportType) {
      case 'daily':
        return (
          <DatePicker
            value={selectedDate}
            onChange={(date) => date && setSelectedDate(date)}
            allowClear={false}
          />
        );
      case 'weekly':
        return (
          <DatePicker.WeekPicker
            value={selectedWeek[0]}
            onChange={(date) =>
              date && setSelectedWeek([date.startOf('isoWeek'), date.endOf('isoWeek')])
            }
            allowClear={false}
          />
        );
      case 'monthly':
        return (
          <DatePicker.MonthPicker
            value={selectedMonth}
            onChange={(date) => date && setSelectedMonth(date)}
            allowClear={false}
          />
        );
      case 'custom':
        return (
          <RangePicker
            value={customDateRange}
            onChange={(dates) =>
              dates && dates[0] && dates[1] && setCustomDateRange([dates[0], dates[1]])
            }
            allowClear={false}
          />
        );
      default:
        return null;
    }
  };

  /**
   * 渲染趋势数据
   */
  const renderTrendData = () => {
    const report = getCurrentReport();
    if (!report) return [];

    if (reportType === 'weekly' && report.daily_data) {
      return report.daily_data.map((item) => ({
        key: item.date,
        period: item.date,
        income: item.income,
        expense: item.expense,
        profit: item.profit,
      }));
    }

    if (reportType === 'monthly' && report.weekly_data) {
      return report.weekly_data.map((item) => ({
        key: item.week.toString(),
        period: `第${item.week}周`,
        income: item.income,
        expense: item.expense,
        profit: item.profit,
      }));
    }

    return [];
  };

  /**
   * 渲染分类明细表格
   */
  const renderCategoryTable = (
    categories: Record<string, number>,
    total: number,
    title: string
  ) => {
    const data = Object.entries(categories).map(([name, amount], index) => ({
      key: index,
      name,
      amount,
      percentage: total > 0 ? ((amount / total) * 100).toFixed(1) : '0.0',
    }));

    const columns = [
      {
        title: '分类名称',
        dataIndex: 'name',
        key: 'name',
      },
      {
        title: '金额',
        dataIndex: 'amount',
        key: 'amount',
        render: (value: number) => `¥${value.toFixed(2)}`,
      },
      {
        title: '占比',
        dataIndex: 'percentage',
        key: 'percentage',
        render: (value: string) => `${value}%`,
      },
    ];

    return (
      <Card title={title} style={{ marginTop: 16 }}>
        <Table
          dataSource={data}
          columns={columns}
          pagination={false}
          size="small"
          locale={{ emptyText: '暂无数据' }}
        />
      </Card>
    );
  };

  const report = getCurrentReport();

  return (
    <div className="p-6">
      <Card>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">经营报表</h2>
          <Space>
            {renderDatePicker()}
            <Dropdown menu={{ items: exportMenuItems }} placement="bottomRight">
              <Button type="primary" icon={<DownloadOutlined />}>
                导出报表
              </Button>
            </Dropdown>
          </Space>
        </div>

        <Tabs
          activeKey={reportType}
          onChange={(key) => setReportType(key as ReportType)}
          items={[
            { key: 'daily', label: '今日' },
            { key: 'weekly', label: '本周' },
            { key: 'monthly', label: '本月' },
            { key: 'custom', label: '自定义' },
          ]}
        />

        <Spin spinning={isLoading}>
          {report && (
            <>
              <Row gutter={16} style={{ marginBottom: 24 }}>
                <Col span={6}>
                  <Card>
                    <Statistic
                      title="总收入"
                      value={report.income}
                      precision={2}
                      prefix="¥"
                      valueStyle={{ color: '#52c41a' }}
                      suffix={<ArrowUpOutlined />}
                    />
                  </Card>
                </Col>
                <Col span={6}>
                  <Card>
                    <Statistic
                      title="总支出"
                      value={report.expense}
                      precision={2}
                      prefix="¥"
                      valueStyle={{ color: '#f5222d' }}
                      suffix={<ArrowDownOutlined />}
                    />
                  </Card>
                </Col>
                <Col span={6}>
                  <Card>
                    <Statistic
                      title="净利润"
                      value={report.profit}
                      precision={2}
                      prefix="¥"
                      valueStyle={{ color: report.profit >= 0 ? '#52c41a' : '#f5222d' }}
                    />
                  </Card>
                </Col>
                <Col span={6}>
                  <Card>
                    <Statistic
                      title="订单数量"
                      value={report.order_count}
                      prefix={<ShoppingCartOutlined />}
                    />
                  </Card>
                </Col>
              </Row>

              {(reportType === 'weekly' || reportType === 'monthly') && (
                <Card title="趋势数据" style={{ marginBottom: 16 }}>
                  <Table
                    dataSource={renderTrendData()}
                    columns={[
                      {
                        title: reportType === 'weekly' ? '日期' : '周',
                        dataIndex: 'period',
                        key: 'period',
                      },
                      {
                        title: '收入',
                        dataIndex: 'income',
                        key: 'income',
                        render: (value: number) => (
                          <span style={{ color: '#52c41a' }}>¥{value.toFixed(2)}</span>
                        ),
                      },
                      {
                        title: '支出',
                        dataIndex: 'expense',
                        key: 'expense',
                        render: (value: number) => (
                          <span style={{ color: '#f5222d' }}>¥{value.toFixed(2)}</span>
                        ),
                      },
                      {
                        title: '利润',
                        dataIndex: 'profit',
                        key: 'profit',
                        render: (value: number) => (
                          <span style={{ color: value >= 0 ? '#52c41a' : '#f5222d' }}>
                            ¥{value.toFixed(2)}
                          </span>
                        ),
                      },
                    ]}
                    pagination={false}
                    size="small"
                    locale={{ emptyText: '暂无数据' }}
                  />
                </Card>
              )}

              <Row gutter={16}>
                <Col span={12}>
                  {renderCategoryTable(
                    report.income_categories,
                    report.income,
                    '收入分类明细'
                  )}
                </Col>
                <Col span={12}>
                  {renderCategoryTable(
                    report.expense_categories,
                    report.expense,
                    '支出分类明细'
                  )}
                </Col>
              </Row>
            </>
          )}

          {!report && !isLoading && (
            <div className="text-center py-12 text-gray-400">暂无报表数据</div>
          )}
        </Spin>
      </Card>
    </div>
  );
};

export default ReportPage;
