resource "aws_glue_crawler" "tdl_lan_cmbs_mkt_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-CMBS-Mkt-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/mktRpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/mktRptHist/"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/mktRptHist_ext1/"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-CMBS-Mkt-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_cur_cmbs_mkt_rpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-CMBS-Mkt-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/mktrpt"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-CUR-CMBS-Mkt-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_lan_cmbs_bond_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-CMBS-Bond-RPT-${var.env}"
  schedule      = "cron(00 */4 ? * * *)"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/bondRpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/bondRptCalc/"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/bondRpt_comp"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/bondBECDR/"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-CMBS-Bond-RPT-${var.env}"
    }
  )
}

/*resource "aws_glue_crawler" "tdl_cur_cmbs_bond_rpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-CMBS-Bond-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/bondrpt"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
}*/

resource "aws_glue_crawler" "tdl_lan_cmbs_deal_settlement_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-CMBS-Deal-SettlementDate-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
      path       = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/treppCMBSSettlementDate"
      exclusions = ["*.crc", "_*"]
      sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-CMBS-Deal-SettlementDate-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_cur_cmbs_deal_settelment_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-CMBS-Deal-SettlementDate-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/treppcmbssettlementdate"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-CUR-CMBS-Deal-SettlementDate-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_lan_cmbs_deal_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-CMBS-Deal-RPT-${var.env}"
  schedule      = "cron(00 */6 ? * * *)"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/dealRpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/dealRptCalc"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
      path       = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/treppCMBSSettlementDate"
      exclusions = ["*.crc", "_*"]
      sample_size = 1
  }
  s3_target {
        path       = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/triggersRpt"
        exclusions = ["*.crc", "_*"]
        sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-CMBS-Deal-RPT-${var.env}"
    }
  )
}

/*resource "aws_glue_crawler" "tdl_cur_cmbs_deal_rpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-CMBS-Deal-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/dealrpt"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
}*/

resource "aws_glue_crawler" "tdl_lan_cmbs_note_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-CMBS-Note-RPT-${var.env}"
  schedule      = "cron(00 */4 ? * * *)"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/notesDat"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-CMBS-Note-RPT-${var.env}"
    }
  )
}

/*resource "aws_glue_crawler" "tdl_cur_cmbs_note_rpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-CMBS-Note-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/noterpt"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
}*/

resource "aws_glue_crawler" "tdl_lan_cmbs_loan_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-CMBS-Loan-RPT-${var.env}"
  schedule      = "cron(00 */6 ? * * *)"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/loanRpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/loanRpt_ext1"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/loanRpt_ext2"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/loanRpt_ext3"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/loanRpt_ext4"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/loanRpt_ext5"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/loanRpt_split"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/loanRptCalc"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/loanRptCalcFullUpd"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/loanDisposition"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/loanDisposition_retiredDeals"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/first_american_loans"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
      path       = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/compassUnqTimeSeries"
      exclusions = ["*.crc", "_*"]
      sample_size = 1
  }
  s3_target {
        path       = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/KBRALoan"
        exclusions = ["*.crc", "_*"]
        sample_size = 1
  }
  s3_target {
          path       = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/morningstarLoan"
          exclusions = ["*.crc", "_*"]
          sample_size = 1
  }
  s3_target {
            path       = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/OSARLatestPeriods"
            exclusions = ["*.crc", "_*"]
            sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-CMBS-Loan-RPT-${var.env}"
    }
  )
}

/*resource "aws_glue_crawler" "tdl_cur_cmbs_loan_rpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-CMBS-Loan-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/loanrpt"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
}*/

resource "aws_glue_crawler" "tdl_lan_cmbs_prop_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-CMBS-Prop-RPT-${var.env}"
  schedule      = "cron(00 */6 ? * * *)"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/propRpt/"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/propRpt_ext1"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/propRpt_ext2"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/propRptCalcFullUpd"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/propRptCalc"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/lpsComparableSale"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/lpsAssessment"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-CMBS-Prop-RPT-${var.env}"
    }
  )
}

/*resource "aws_glue_crawler" "tdl_cur_cmbs_prop_rpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-CMBS-Prop-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/proprpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
}*/

resource "aws_glue_crawler" "tdl_lan_cmbs_dealsExcludeVerify_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-CMBS-dealsExcludeVerify-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/loadDb_dealsExcludeVerification"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-CMBS-dealsExcludeVerify-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_cur_cmbs_dealsExcludeVerify_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-CMBS-dealsExcludeVerify-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/dealsExcludeVerification"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-CUR-CMBS-dealsExcludeVerify-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_per_cmbs_dealsExcludeVerify_crawler" {
  database_name = var.presentation_database
  name          = "TDL-PRESENTATION-CMBS-dealsExcludeVerify-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/presentationZone/cmbs/dealsExcludeVerification"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-PRESENTATION-CMBS-dealsExcludeVerify-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_lan_cmbs_excludeDatafeedDeals_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-CMBS-ExcludeDatafeedDeals-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/excludeDatafeedDeals"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-CMBS-ExcludeDatafeedDeals-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_cur_cmbs_excludeDatafeedDeals_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-CMBS-ExcludeDatafeedDeals-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/excludeDatafeedDeals"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-CUR-CMBS-ExcludeDatafeedDeals-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_per_cmbs_excludeDatafeedDeals_crawler" {
  database_name = var.presentation_database
  name          = "TDL-PRESENTATION-CMBS-excludeDatafeedDeals-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/presentationZone/cmbs/excludeDatafeedDeals"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-PRESENTATION-CMBS-excludeDatafeedDeals-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_lan_cmbs_pinrpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-CMBS-PINRPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/pinRpt"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-CMBS-PINRPT-${var.env}"
    }
  )
}

/*resource "aws_glue_crawler" "tdl_cur_cmbs_pinrpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-CMBS-PINRPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/pinrpt"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
}*/

resource "aws_glue_crawler" "tdl_cur_cmbsdelta_pinrpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-DELTACMBS-PINRPT-${var.env}"
  table_prefix  = "cmbs"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/pinrpt"
    exclusions = ["*.crc", "_*"]
  }
  schema_change_policy {
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-CUR-DELTACMBS-PINRPT-${var.env}"
    }
  )
}
resource "aws_glue_crawler" "tdl_lan_cmbsdelta_bond_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-DELTACMBS-Bond-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path       = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/bondRpt"
    exclusions = ["*.crc", "_*"]
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/bondRptCalc"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-DELTACMBS-Bond-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_lan_cmbsdelta_deal_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-DELTACMBS-Deal-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/dealRpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/dealRptCalc"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }

  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-DELTACMBS-Deal-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_lan_cmbsdelta_note_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-DELTACMBS-Note-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/notesDat"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-DELTACMBS-Note-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_lan_cmbs_cmbsdealindices_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-CMBSDEALINDICES-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = ""
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/cmbsDealIndices"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-CMBSDEALINDICES-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_lan_cmbsdelta_loan_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-DELTACMBS-Loan-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/loanRpt_ext1"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/loanRpt_ext2"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/loanRpt_ext3"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/loanRpt_ext4"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/loanRpt_ext5"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/loanRpt_split"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/loanRpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/loanRptCalc"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/loanRptCalcFullUpd"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-DELTACMBS-Loan-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_lan_cmbsdelta_mkt_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-DELTACMBS-Mkt-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/mktRpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/mktRptHist_ext1"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/mktRptHist"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-DELTACMBS-Mkt-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_lan_cmbsdelta_prop_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-DELTACMBS-Prop-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/propRpt_ext1"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/propRpt_ext2"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/propRpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/propRptCalc"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/propRptCalcFullUpd"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-DELTACMBS-Prop-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_cur_cmbsdelta_bond_rpt_crawler_deal_rpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-DELTACMBS-Deal-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/dealrpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-CUR-DELTACMBS-Deal-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_cur_cmbsdelta_bond_rpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-DELTACMBS-Bond-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/bondrpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-CUR-DELTACMBS-Bond-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_cur_cmbsdelta_mkt_rpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-DELTACMBS-Mkt-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/mktrpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-CUR-DELTACMBS-Mkt-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_cur_cmbsdelta_note_rpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-DELTACMBS-Note-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/noterpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-CUR-DELTACMBS-Note-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_cur_cmbsdelta_prop_rpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-DELTACMBS-Prop-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/proprpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-CUR-DELTACMBS-Prop-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_cur_cmbsdelta_loan_rpt_crawler" {
  database_name = var.curation_database
  name          = "TDL-CUR-DELTACMBS-Loan-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/curationZone/cmbs/loanrpt"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-CUR-DELTACMBS-Loan-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_lan_cmbsmappingtables_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-CMBSMAPPING-TABLES-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/msaMap_msaName_consistent"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/derivedFinancialCodeMap"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/amortTypeStratCats"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-CMBSMAPPING-TABLES-RPT-${var.env}"
    }
  )
}

resource "aws_glue_crawler" "tdl_deltaoverrideloandat_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-DELTAOVERRIDELOANDAT-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/treppwebdb3/dbo/overrideLoanDat"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-DELTAOVERRIDELOANDAT-RPT-${var.env}"
    }
  )
}
resource "aws_glue_crawler" "tdl_overrideloandat_rpt_crawler" {
  database_name = var.landing_database
  name          = "TDL-LAN-OVERRIDELOANDAT-Loan-RPT-${var.env}"
  role          = var.glue_role
  configuration = file("${path.module}/templates/cmbsfeed_configuration.json")
  table_prefix  = "cmbs"
  s3_target {
    path        = "s3://${var.glue_bucket[var.s3_alias]}/landingZone/archivedb/dbo/overrideLoanDat/"
    exclusions  = ["*.crc", "_*"]
    sample_size = 1
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  tags = merge(
    var.tags,
    {
      eng-environment            = var.env
      eng-product-component-name = "TDL-LAN-OVERRIDELOANDAT-Loan-RPT-${var.env}"
    }
  )
}
