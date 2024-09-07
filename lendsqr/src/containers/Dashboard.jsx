import React, { useState, useEffect, useCallback } from "react";
import styled from "styled-components";
import SideBar from "../components/SideBar";
import Users from "../components/Users";
import NavBar from "../components/NavBar";
import axios from "axios";
import { motion } from "framer-motion";
import Loading from "../components/Loading";
import { logout } from "../action/auth";
import { connect } from "react-redux";
import { UserContext } from "../components/ContextManager";
import { mergeFields } from "../components/utility/AdminAction";

const Container = styled.div`
  padding: 8px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  overflow-x: hidden;
  @media screen and (max-width: 568px) {
    overflow-x: auto;
  }
`;

const Left = styled.div`
  position: relative;
`;

const Right = styled.div`
  width: 75%;
  @media screen and (max-width: 568px) {
    width: 100%;
    margin: 5px;
  }
`;

const Dashstats = styled.div`
  margin-left: 0px;
  margin-bottom: 20px;
  margin-top: 20px;
  display: flex;
  align: items: center;
  justify-content: center;
  flex-wrap: wrap;
  padding: 10px;
  flex: 12;
  @media screen and (min-width: 0px) and (max-width: 568px) {
    flex-wrap: nowrap;
    flex-basis: 24%;
  }
`;

const Stats = styled.div`
  background-color: white;
  height: 160px;
  width: 240px;
  border: 1px solid rgba(33, 63, 125, 0.06);
  box-shadow: 3px 5px 20px rgba(0, 0, 0, 0.04);
  border-radius: 4px;
  flex: 3;
  justify-content: flex-start;
  align-items: left;
  display: flex;
  flex-direction: column;
  margin: 5px;
  padding: 12px 10px;
`;

const StatIcon = styled.img`
  height: 25%;
  width: 25%;
  border-radius: 50%;
`;

const StatDesc = styled.h5`
  font-family: "Work Sans";
  font-style: normal;
  font-weight: bold;
  font-size: 14px;
  line-height: 16px;
  text-transform: uppercase;
  color: #0050b5;
  margin-top: 5px;
`;

const StatNum = styled.h5`
  font-family: "Work Sans";
  font-style: normal;
  font-weight: 600;
  font-size: 24px;
  line-height: 28px;
  text-transform: uppercase;
  margin-top: 3px;
  color: #0050b5;
  opacity: 1;
`;

const ADVANCE_FILTER_URL = "/api/advance-filter";
const USERS_URL = "/api/users";

const Dashboard = ({ logout }) => {
  window.title = "Dashboard";
  const token = localStorage.getItem("access");
  const [searchValue, setSearchValue] = useState("");
  const [page, setPage] = useState(1);
  const [modal, setModal] = useState(false);
  const [error, setError] = useState("");
  const [statusUpdated, setStatusUpdated] = useState(false);
  const [raw, setRaw] = useState({
    items: {
      users_paginated: [],
      all_users: 0,
      active: 0,
      loan: 0,
      savings: 0,
    },
  });
  const [clicked, setClicked] = useState(false);
  const [inputs, setInputs] = useState({});
  const [filtered, setFiltered] = useState(0);
  const PageSize = inputs.itemCount || 20;
  const [display, setDisplay] = useState(false);

  const handleChange = useCallback(
    (item) => {
      setInputs(item);
    },
    [setInputs]
  );

  const onFilter = useCallback(() => {
    setFiltered((prev) => prev + 1);
  }, []);

  const onReset = useCallback(() => {
    setInputs({});
    setFiltered(0);
  }, []);

  const filterClick = useCallback(() => {
    setClicked((prev) => !prev);
  }, []);

  const onMenuClick = useCallback(() => {
    setDisplay((prev) => !prev);
  }, []);

  const updateStatus = useCallback(() => {
    setStatusUpdated((prev) => !prev);
  }, []);

  const nextPage = useCallback(() => {
    if (page < Math.ceil(raw.items.all_users / PageSize)) {
      setModal(true);
      setPage((prev) => prev + 1);
      window.scrollTo({ top: 300, behavior: "smooth" });
    }
  }, [page, raw.items.all_users, PageSize]);

  const prevPage = useCallback(() => {
    if (page > 1) {
      setModal(true);
      setPage((prev) => prev - 1);
      window.scrollTo({ top: 300, behavior: "smooth" });
    }
  }, [page]);

  const HandleInputChange = useCallback(
    (event) => {
      setSearchValue(event.target.value);
    },
    [setSearchValue]
  );

  useEffect(() => {
    const config = {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `JWT ${token}`,
        Accept: "application/json",
      },
    };
    let search = "";
    if (searchValue.length >= 4) {
      search = searchValue;
    }

    if (token) {
      const fetchData = async () => {
        try {
          if (clicked && filtered) {
            const profileKeys = ["userName", "status", "email", "phoneNumber"];
            const organizationKeys = ["orgName"];
            const profile = mergeFields(inputs, profileKeys);
            const organization = mergeFields(inputs, organizationKeys);

            const response = await axios.get(
              `${ADVANCE_FILTER_URL}?page=${page}&pageSize=${PageSize}`,
              {
                params: {
                  profile: JSON.stringify({ profile }),
                  organization: JSON.stringify({ organization }),
                },
                ...config,
              }
            );
            setModal(false);
            setRaw({ items: response.data });
          } else {
            const response = await axios.get(
              `${USERS_URL}?page=${page}&pageSize=${PageSize}&search=${search}`,
              config
            );
            setModal(false);
            setRaw({ items: response.data });
          }
        } catch (error) {
          setModal(false);
          setError(error);
          logout();
        }
      };

      fetchData();
    } else {
      logout();
    }
  }, [
    page,
    logout,
    token,
    searchValue,
    statusUpdated,
    filtered,
    inputs,
    clicked,
    PageSize,
  ]);

  return (
    <UserContext.Provider value={raw.items}>
      <motion.div
        initial={{ scale: 0 }}
        animate={{ rotate: 0, scale: 1 }}
        transition={{
          type: "spring",
          stiffness: 260,
          damping: 20,
        }}
      >
        <Container>
          <Left className={display ? "appear" : "disappear"}>
            <SideBar />
          </Left>
          <Right>
            <NavBar
              searchValue={searchValue}
              HandleInputChange={HandleInputChange}
              onMenuClick={onMenuClick}
            />
            <div style={{ backgroundColor: "whitesmoke" }}>
              <h3
                style={{
                  color: "#0050B5",
                  marginLeft: "10px",
                  paddingTop: "25px",
                }}
              >
                Users
              </h3>
              <Dashstats>
                <Stats>
                  <StatIcon src="/static/icons/user.png" alt="user" />
                  <StatDesc>users</StatDesc>
                  <StatNum>{raw.items.all_users}</StatNum>
                </Stats>
                <Stats>
                  <StatIcon
                    src="/static/icons/user_active.png"
                    alt="active icon"
                  />
                  <StatDesc>ACTIVE USERS</StatDesc>
                  <StatNum>{raw.items.active}</StatNum>
                </Stats>
                <Stats>
                  <StatIcon src="/static/icons/user_loan.png" alt="loan icon" />
                  <StatDesc>USERS WITH LOANS</StatDesc>
                  <StatNum>{raw.items.loan}</StatNum>
                </Stats>
                <Stats>
                  <StatIcon
                    src="/static/icons/user_savings.png"
                    alt="savings icon"
                  />
                  <StatDesc>USERS WITH SAVINGS</StatDesc>
                  <StatNum>{raw.items.savings}</StatNum>
                </Stats>
              </Dashstats>
              {error}
              {modal && Loading()}
              <Users
                page={page}
                PageSize={PageSize}
                nextPage={nextPage}
                prevPage={prevPage}
                HandleInputChange={HandleInputChange}
                filterClick={filterClick}
                onFilter={onFilter}
                clicked={clicked}
                setClicked={setClicked}
                filtered={filtered}
                setFiltered={setFiltered}
                onReset={onReset}
                handleChange={handleChange}
                statusUpdated={statusUpdated}
                updateStatus={updateStatus}
                inputs={inputs}
              />
            </div>
          </Right>
        </Container>
      </motion.div>
    </UserContext.Provider>
  );
};

const mapDispatchToProps = (dispatch) => ({
  logout: () => dispatch(logout()),
});

export default connect(null, mapDispatchToProps)(React.memo(Dashboard));
